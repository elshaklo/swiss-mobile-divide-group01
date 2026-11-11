"""Reproducible spatial integration, SQLite, EDA, inference and prediction.

No simulated observations. Missing speed measurements remain missing.
The unit of the final analysis is a municipality, NOT an individual test.
"""
from pathlib import Path
import json, sqlite3, zipfile, warnings
import numpy as np
import pandas as pd
import geopandas as gpd
import shapely
from scipy import stats
import statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.diagnostic import het_breuschpagan
from sklearn.model_selection import train_test_split, GroupKFold
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error, silhouette_score, adjusted_rand_score
from sklearn.cluster import KMeans
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'data/raw'; OUT=ROOT/'data/processed'; RES=ROOT/'results'
ORDER=['Urban','Intermediate','Rural']
COLORS=['#086788','#e9a23b','#984c80']
SEED=42
AUDIT=[]
def audit(step,n,detail): AUDIT.append({'step':step,'records':int(n),'detail':detail})
def save_json(name,obj):
    (RES/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2,default=lambda x:float(x) if isinstance(x,np.generic) else str(x),allow_nan=False))
def fig(name):
    plt.savefig(RES/name,dpi=180,bbox_inches='tight',facecolor='white');plt.close()

def spatial_join(points,municipalities,key):
    """Within assigns at most one unit; boundary cases choose lowest BFS id.
    No nearest-neighbour snapping across national borders.
    """
    joined=gpd.sjoin(points,municipalities[['bfs_id','geometry']],how='left',predicate='within').drop(columns='index_right')
    ambiguous=joined[key].duplicated().sum()
    if ambiguous: raise ValueError(f'Unexpected overlapping polygons: {ambiguous}')
    missing=joined[joined.bfs_id.isna()].drop(columns='bfs_id')
    candidates=gpd.sjoin(missing,municipalities[['bfs_id','geometry']],how='inner',predicate='intersects')
    if len(candidates):
        candidates=candidates.sort_values('bfs_id').drop_duplicates(key)
        mapping=candidates.set_index(key).bfs_id
        joined['bfs_id']=joined.bfs_id.fillna(joined[key].map(mapping))
    audit(key+'_boundary_assignments',len(candidates),'Exact boundary intersects, smallest BFS id; no nearest snapping')
    return joined

def integrate():
    unpack=OUT/'boundaries';unpack.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(RAW/'boundaries_2026.gpkg.zip') as z:z.extractall(unpack)
    geo=gpd.read_file(next(unpack.glob('*.gpkg')),layer='tlm_hoheitsgebiet')
    audit('boundary_all_features',len(geo),'Includes lakes and foreign units')
    geo=geo[(geo.icc=='CH')&(geo.objektart=='Gemeindegebiet')].copy()
    geo['geometry']=shapely.force_2d(geo.geometry.make_valid())
    geo['bfs_id']=geo.bfs_nummer.astype(int)
    geo=geo.dissolve(by='bfs_id',aggfunc={'name':'first','kantonsnummer':'first','gem_flaeche':'max'}).reset_index()
    geo=geo.rename(columns={'name':'municipality','kantonsnummer':'canton','gem_flaeche':'area_ha'})
    geo['area_km2']=geo.area_ha/100
    audit('boundary_swiss_municipalities',len(geo),'Dissolved BFS id; exclude lakes/foreign units')
    types=pd.read_csv(RAW/'bfs_typologies_labels_2026.csv')
    types=types[['BfsCode','STALAN2020','STALAN2020_de','MONT2019']].rename(columns={'BfsCode':'bfs_id','STALAN2020':'type_code','STALAN2020_de':'type_official','MONT2019':'mountain'})
    assert types.bfs_id.is_unique and geo.bfs_id.is_unique
    missing_types=geo.loc[~geo.bfs_id.isin(types.bfs_id),['bfs_id','municipality']]
    missing_types.to_csv(RES/'unmatched_typology.csv',index=False)
    geo=geo.merge(types,on='bfs_id',how='left',validate='one_to_one')
    audit('municipalities_missing_typology',geo.type_code.isna().sum(),'Left join on integer BFS id, no municipality discarded')
    geo['municipality_type']=geo.type_code.map({1:'Urban',2:'Intermediate',3:'Rural'})
    pop=json.loads((RAW/'population_2025.json').read_text())
    cat=pop['dimension'][pop['id'][1]]['category']
    population=pd.DataFrame([{'bfs_id':int(k),'population':pop['value'][i]} for k,i in cat['index'].items()])
    population_total=population.population.sum()
    audit('population_source_municipalities',len(population),'Population uses geography 2025-04-06; harmonize before joining')
    correspondence=pd.read_csv(RAW/'municipality_correspondences_2025_2026.csv')
    links=correspondence[['InitialCode','TerminalCode']].drop_duplicates()
    if not links.InitialCode.is_unique:raise ValueError('One-to-many municipality change needs explicit population allocation')
    population=population.merge(links,left_on='bfs_id',right_on='InitialCode',how='left',validate='one_to_one')
    assert population.TerminalCode.notna().all()
    audit('population_changed_municipality_codes',population.bfs_id.ne(population.TerminalCode).sum(),'Official BFS correspondences incl. mergers and Moutier canton transfer')
    population=population.groupby('TerminalCode',as_index=False).population.sum().rename(columns={'TerminalCode':'bfs_id'})
    assert population.population.sum()==population_total
    audit('population_harmonized_municipalities',len(population),'Aggregate many-to-one mergers; population total conserved')
    population.to_csv(OUT/'population_2025.csv',index=False)
    geo=geo.merge(population,on='bfs_id',how='left',validate='one_to_one')
    audit('municipalities_missing_population',geo.population.isna().sum(),'No ad hoc name matching or population imputation')
    population.loc[~population.bfs_id.isin(geo.bfs_id)].to_csv(RES/'population_unmatched_ids.csv',index=False)
    geo['population_density']=geo.population/geo.area_km2
    ant=gpd.read_file(RAW/'bakom_stations_2026-11-09.geojson').to_crs(2056)
    audit('station_records_raw',len(ant),'Operator station records, not individual antenna elements or unique physical masts')
    ant['record_key']=ant.station.astype(str)+'|'+ant.koord.astype(str)
    duplicates=ant.record_key.duplicated().sum()
    ant=ant.drop_duplicates('record_key').copy()
    audit('station_exact_duplicates_removed',duplicates,'Deduplicate station identifier plus coordinates only')
    ant['has_5g']=ant.techno_de.fillna('').str.contains('5G',regex=False).astype(int)
    ant['outdoor']=(ant.typ_de=='Outdoor > 6 Werp').astype(int)
    ant=spatial_join(ant,geo,'record_key')
    audit('stations_not_in_municipality',ant.bfs_id.isna().sum(),'Retained in unmatched output; may be foreign/on unallocated lake territory')
    ant.loc[ant.bfs_id.isna()].drop(columns='geometry').to_csv(RES/'stations_unmatched.csv',index=False)
    ant=ant[ant.bfs_id.notna()].copy();ant.bfs_id=ant.bfs_id.astype(int)
    outdoor=ant[ant.outdoor.eq(1)]
    infra=outdoor.groupby('bfs_id').agg(stations=('record_key','size'),stations_5g=('has_5g','sum')).reset_index()
    infra_all=ant.groupby('bfs_id').size().rename('stations_all').reset_index()
    geo=geo.merge(infra,on='bfs_id',how='left',validate='one_to_one').merge(infra_all,on='bfs_id',how='left',validate='one_to_one')
    for c in ['stations','stations_5g','stations_all']:geo[c]=geo[c].fillna(0).astype(int)
    geo['station_density']=geo.stations/geo.area_km2
    geo['station_density_all']=geo.stations_all/geo.area_km2
    geo['share_5g']=geo.stations_5g/geo.stations.replace(0,np.nan)
    geo['no_station']=(geo.stations==0).astype(int)
    geo['share_5g_model']=geo.share_5g.fillna(0)
    tiles=pd.read_parquet(RAW/'ookla_bbox_q3_2026.parquet')
    audit('ookla_bbox_tiles',len(tiles),'BBox contains foreign tiles; not yet Switzerland-only')
    assert tiles.quadkey.is_unique
    valid=(tiles.tests>0)&(tiles.devices>0)&(tiles.avg_d_kbps>0)&(tiles.avg_u_kbps>=0)&(tiles.avg_lat_ms>=0)
    audit('invalid_tiles_removed',(~valid).sum(),'Positive test/device counts and download, nonnegative upload/latency')
    tiles=tiles[valid].copy()
    for col,source in [('download_mbps','avg_d_kbps'),('upload_mbps','avg_u_kbps')]:tiles[col]=tiles[source]/1000
    tiles['latency_ms']=tiles.avg_lat_ms
    points=gpd.GeoDataFrame(tiles,geometry=gpd.points_from_xy(tiles.tile_x,tiles.tile_y),crs=4326).to_crs(2056)
    points=spatial_join(points,geo,'quadkey')
    audit('ookla_tiles_outside_municipalities',points.bfs_id.isna().sum(),'Foreign, lake and border-centroid tiles excluded; not missing-speed zeros')
    points=points[points.bfs_id.notna()].copy();points.bfs_id=points.bfs_id.astype(int)
    # A tile touching a border may contain tests on both sides. Sensitivity
    # excludes every tile polygon not wholly contained in its assigned municipality.
    polys=gpd.GeoSeries.from_wkt(points.tile,crs=4326).to_crs(2056)
    bounds=geo.set_index('bfs_id').geometry
    points['fully_inside']=[bounds.loc[b].covers(p) for b,p in zip(points.bfs_id,polys)]
    audit('ookla_assigned_tiles',len(points),'Centroid within municipality; boundary sensitivity also computed')
    performance=points.drop(columns='geometry').groupby('bfs_id').apply(lambda x:pd.Series({
        'download_mbps':np.average(x.download_mbps,weights=x.tests),
        'upload_mbps':np.average(x.upload_mbps,weights=x.tests),
        'latency_ms':np.average(x.latency_ms,weights=x.tests),
        'download_unweighted':x.download_mbps.mean(),
        'tests':x.tests.sum(),'devices_sum':x.devices.sum(),'tile_count':len(x),
    }),include_groups=False).reset_index()
    # devices_sum is NOT a count of unique people/devices across tiles.
    safe=points[points.fully_inside].groupby('bfs_id').apply(lambda x:np.average(x.download_mbps,weights=x.tests),include_groups=False).rename('download_inside').reset_index()
    performance=performance.merge(safe,on='bfs_id',how='left',validate='one_to_one')
    frame=geo.merge(performance,on='bfs_id',how='left',validate='one_to_one')
    frame['observed']=frame.download_mbps.notna()
    frame['eligible']=(frame.observed & frame.tests.ge(30)&frame.tile_count.ge(3)&frame.population.gt(0)&frame.municipality_type.notna())
    audit('all_integrated_municipalities',len(frame),'One row per municipality, unobserved outcome stays NULL')
    audit('observed_municipalities',frame.observed.sum(),'At least one valid mobile tile')
    audit('eligible_municipalities',frame.eligible.sum(),'Predefined >=30 tests, >=3 tiles; population >0 and known typology')
    for c in ['station_density','station_density_all','population_density']:frame['log_'+c]=np.log1p(frame[c])
    frame['log_download']=np.log(frame.download_mbps)
    frame['canton']=frame.canton.astype(int)
    frame.drop(columns='geometry').to_csv(OUT/'municipalities.csv',index=False)
    frame.to_parquet(OUT/'municipalities.parquet',index=False)
    points.drop(columns='geometry').to_parquet(OUT/'tiles_assigned.parquet',index=False)
    ant.drop(columns='geometry').to_csv(OUT/'stations_assigned.csv',index=False)
    # Normalized source tables, SQL join/aggregation in Python for baseline.
    con=sqlite3.connect(OUT/'mobile_divide.sqlite')
    pd.DataFrame(frame.drop(columns='geometry')).to_sql('municipalities',con,index=False,if_exists='replace')
    pd.DataFrame(points.drop(columns='geometry')).to_sql('tiles',con,index=False,if_exists='replace')
    pd.DataFrame(ant.drop(columns='geometry')).to_sql('stations',con,index=False,if_exists='replace')
    sql='''SELECT m.municipality_type, COUNT(DISTINCT m.bfs_id) AS municipalities,
    COUNT(t.quadkey) AS tiles, SUM(t.tests) AS tests,
    SUM(t.download_mbps*t.tests)/SUM(t.tests) AS test_weighted_download_mbps
    FROM municipalities m JOIN tiles t ON m.bfs_id=t.bfs_id
    GROUP BY m.municipality_type ORDER BY m.municipality_type'''
    pd.read_sql_query(sql,con).to_csv(RES/'sqlite_query_result.csv',index=False)
    (ROOT/'src/group_summary.sql').write_text(sql+';\n')
    con.close()
    pd.DataFrame(AUDIT).to_csv(RES/'integration_audit.csv',index=False)
    return frame,points

def describe(frame,points):
    df=frame[frame.eligible].copy()
    cols=['download_mbps','upload_mbps','latency_ms','station_density','share_5g','population_density','tests','tile_count']
    df[cols].describe(percentiles=[.05,.25,.5,.75,.95]).to_csv(RES/'descriptive_statistics.csv')
    frame.drop(columns='geometry').isna().sum().rename('missing').to_csv(RES/'missing_values.csv')
    summary=frame.groupby('municipality_type',observed=True).agg(total=('bfs_id','size'),observed=('observed','sum'),eligible=('eligible','sum'))
    summary['observed_pct']=100*summary.observed/summary.total
    summary['eligible_pct']=100*summary.eligible/summary.total
    summary.to_csv(RES/'coverage_by_type.csv')
    groups=df.groupby('municipality_type').agg(n=('bfs_id','size'),mean_download=('download_mbps','mean'),median_download=('download_mbps','median'),mean_upload=('upload_mbps','mean'),median_latency=('latency_ms','median'),median_density=('station_density','median'))
    groups.to_csv(RES/'group_summary.csv')
    sns.set_theme(style='whitegrid',font='Arial',font_scale=1.08)
    plt.figure(figsize=(8,5));sns.boxplot(data=df,x='municipality_type',y='download_mbps',order=ORDER,hue='municipality_type',palette=dict(zip(ORDER,COLORS)),legend=False,showfliers=False)
    plt.xlabel('Municipality type (BFS 2020)');plt.ylabel('Test-weighted municipality download (Mbps)');plt.title('Observed mobile download speeds | 2026 Q3');fig('download_by_type.png')
    plt.figure(figsize=(8,5));sns.scatterplot(data=df,x='station_density',y='download_mbps',hue='municipality_type',hue_order=ORDER,palette=COLORS,alpha=.55,s=22)
    plt.xscale('symlog',linthresh=.05);plt.xlabel('Outdoor station records per km² (symlog)');plt.ylabel('Download (Mbps)');fig('density_download.png')
    plt.figure(figsize=(8,6));sns.heatmap(df[cols].corr(method='spearman'),annot=True,fmt='.2f',cmap='vlag',center=0,vmin=-1,vmax=1);fig('correlations.png')
    plt.figure(figsize=(8,4));summary.reindex(ORDER)[['observed_pct','eligible_pct']].plot.bar(ax=plt.gca(),color=['#086788','#e9a23b']);plt.ylim(0,105);plt.ylabel('% of municipalities');plt.xlabel('');plt.xticks(rotation=0);plt.legend(['Any measurements','Eligible for model']);fig('coverage_by_type.png')
    ax=frame.plot(column='download_mbps',cmap='viridis',legend=True,figsize=(10,6),vmin=0,vmax=frame.download_mbps.quantile(.95),missing_kwds={'color':'#dddddd','label':'No measurements'},linewidth=0)
    ax.set_axis_off();ax.set_title('Mobile download by municipality (Mbps) | 2026 Q3\nGrey = no observed tiles; scale capped at 95th percentile');fig('swiss_download_map.png')
    ax=frame.plot(column='station_density',cmap='YlOrRd',legend=True,figsize=(10,6),vmin=0,vmax=frame.station_density.quantile(.95),linewidth=0)
    ax.set_axis_off();ax.set_title('Outdoor operator-station records per km² | 9 November 2026\nScale capped at 95th percentile; not a coverage map');fig('swiss_stations_map.png')
    return df,groups,summary

def infer(df,frame):
    samples=[np.log(df.loc[df.municipality_type==g,'download_mbps']) for g in ORDER]
    # Welch ANOVA does not assume equal group variances (SciPy >=1.16).
    welch=stats.f_oneway(*samples,equal_var=False)
    lev=stats.levene(*samples,center='median');kw=stats.kruskal(*samples)
    results={'welch_anova_log_speed':{'statistic':welch.statistic,'p':welch.pvalue},'levene_log_speed':{'statistic':lev.statistic,'p':lev.pvalue},'kruskal_wallis':{'statistic':kw.statistic,'p':kw.pvalue}}
    comparisons=[]
    for a,b in [('Urban','Intermediate'),('Urban','Rural'),('Intermediate','Rural')]:
        aa=np.log(df.loc[df.municipality_type==a,'download_mbps']);bb=np.log(df.loc[df.municipality_type==b,'download_mbps'])
        t=stats.ttest_ind(aa,bb,equal_var=False)
        comparisons.append({'a':a,'b':b,'log_mean_difference':aa.mean()-bb.mean(),'p':t.pvalue})
    adjusted=multipletests([x['p'] for x in comparisons],method='holm')[1]
    for r,p in zip(comparisons,adjusted):r['p_holm']=p
    results['pairwise_welch_holm']=comparisons
    corr=stats.spearmanr(df.station_density,df.download_mbps)
    results['spearman_density_speed']={'rho':corr.statistic,'p':corr.pvalue,'n':len(df)}
    save_json('statistical_tests.json',results)
    base='log_download ~ C(municipality_type, Treatment(reference="Urban")) + log_population_density + mountain'
    extended=base+' + log_station_density + share_5g_model'
    if df.no_station.nunique()>1:extended+=' + no_station'
    formulas={'group_only':'log_download ~ C(municipality_type, Treatment(reference="Urban"))','controls':base,'infrastructure':extended,'canton_sensitivity':extended+' + C(canton)'}
    models={};coeff=[]
    for name,formula in formulas.items():
        m=smf.ols(formula,df).fit(cov_type='cluster',cov_kwds={'groups':df.canton},use_t=True)
        models[name]=m
        (RES/(name+'_ols.txt')).write_text(m.summary().as_text())
        ci=m.conf_int()
        for term in m.params.index:
            coeff.append({'model':name,'term':term,'coef':m.params[term],'ci_low':ci.loc[term,0],'ci_high':ci.loc[term,1],'p':m.pvalues[term]})
    pd.DataFrame(coeff).to_csv(RES/'ols_coefficients.csv',index=False)
    m=models['infrastructure'];bp=het_breuschpagan(m.resid,m.model.exog)
    # Sensitivity to reliability threshold, tile weighting, and border assignment.
    sensitive=[];sensitivity_counts=[]
    for label,d in [('all_observed',frame[frame.observed&frame.population.gt(0)&frame.municipality_type.notna()]),('threshold_10',frame[frame.observed&frame.tests.ge(10)&frame.tile_count.ge(2)&frame.population.gt(0)&frame.municipality_type.notna()]),('threshold_100',frame[frame.eligible&frame.tests.ge(100)]),('unweighted_tiles',df.assign(log_download=np.log(df.download_unweighted))),('interior_tiles',df[df.download_inside.gt(0)].assign(log_download=lambda x:np.log(x.download_inside))),('all_station_types',df.assign(log_station_density=df.log_station_density_all))]:
        counts=d.groupby('municipality_type').size().reindex(ORDER,fill_value=0)
        usable=bool(counts.min()>=10)
        sensitivity_counts.append({'analysis':label,**counts.to_dict(),'model_fitted':usable,'note':'Descriptive threshold check only if any group has fewer than 10 municipalities'})
        if not usable:continue
        formula=extended
        if d.no_station.nunique()>1 and 'no_station' not in formula:formula+=' + no_station'
        fit=smf.ols(formula,d).fit(cov_type='cluster',cov_kwds={'groups':d.canton},use_t=True)
        for term in fit.params.index:
            if 'municipality_type' in term or term=='log_station_density': sensitive.append({'analysis':label,'n':len(d),'term':term,'coef':fit.params[term],'p':fit.pvalues[term]})
    pd.DataFrame(sensitive).to_csv(RES/'sensitivity.csv',index=False)
    pd.DataFrame(sensitivity_counts).to_csv(RES/'sensitivity_group_counts.csv',index=False)
    # Descriptive CI: canton cluster bootstrap of raw Urban-Rural median gap.
    rng=np.random.default_rng(SEED);cantons=df.canton.unique();gaps=[]
    for _ in range(1000):
        d=pd.concat([df[df.canton.eq(c)] for c in rng.choice(cantons,len(cantons),replace=True)])
        med=d.groupby('municipality_type').download_mbps.median()
        if 'Urban' in med and 'Rural' in med:gaps.append(med['Urban']-med['Rural'])
    bootstrap={'estimand':'Urban minus Rural median municipality Mbps','median_gap':df.loc[df.municipality_type.eq('Urban'),'download_mbps'].median()-df.loc[df.municipality_type.eq('Rural'),'download_mbps'].median(),'ci95':np.quantile(gaps,[.025,.975]).tolist(),'resamples':len(gaps),'cluster':'canton','seed':SEED}
    save_json('bootstrap_gap.json',bootstrap)
    plt.figure(figsize=(8,4));plt.scatter(m.fittedvalues,m.resid,s=13,alpha=.4,color=COLORS[0]);plt.axhline(0,color='black',lw=1);plt.xlabel('Fitted log download');plt.ylabel('Residual');fig('residuals.png')
    plt.figure(figsize=(6,5));stats.probplot(m.resid,dist='norm',plot=plt);fig('qq_plot.png')
    save_json('inference_diagnostics.json',{'bp_statistic':bp[0],'bp_p':bp[1],'n_canton_clusters':len(cantons),'caution':'P-values exploratory: 26 clusters and residual spatial dependence remain. Cross-sectional associations do not identify causal effects.'})
    return models,bootstrap

def predict(df):
    numeric=['log_population_density','mountain','log_station_density','share_5g_model','no_station']
    categoric=['municipality_type']
    X=df[numeric+categoric];y=df.download_mbps
    def prep():return ColumnTransformer([('numeric',make_pipeline(SimpleImputer(strategy='median'),StandardScaler()),numeric),('type',OneHotEncoder(handle_unknown='ignore'),categoric)])
    train,test=train_test_split(np.arange(len(df)),test_size=.2,random_state=SEED,stratify=df.municipality_type)
    candidates={'Mean baseline':DummyRegressor(strategy='mean'),'Linear regression':make_pipeline(prep(),LinearRegression()),'Random forest':make_pipeline(prep(),RandomForestRegressor(n_estimators=250,min_samples_leaf=8,max_features=.8,random_state=SEED,n_jobs=2))}
    rows=[];preds=pd.DataFrame({'bfs_id':df.iloc[test].bfs_id.values,'actual_mbps':y.iloc[test].values})
    for name,model in candidates.items():
        model.fit(X.iloc[train],y.iloc[train]);p=model.predict(X.iloc[test]);preds[name]=p
        rows.append({'validation':'Random 80/20 holdout','model':name,'n_test':len(test),'r2':r2_score(y.iloc[test],p),'rmse_mbps':np.sqrt(mean_squared_error(y.iloc[test],p)),'mae_mbps':mean_absolute_error(y.iloc[test],p)})
        cv=GroupKFold(n_splits=5);oof=np.empty(len(df))
        for tr,te in cv.split(X,y,groups=df.canton):
            model.fit(X.iloc[tr],y.iloc[tr]);oof[te]=model.predict(X.iloc[te])
        rows.append({'validation':'5-fold canton-grouped OOF','model':name,'n_test':len(df),'r2':r2_score(y,oof),'rmse_mbps':np.sqrt(mean_squared_error(y,oof)),'mae_mbps':mean_absolute_error(y,oof)})
    scores=pd.DataFrame(rows);scores.to_csv(RES/'model_evaluation.csv',index=False);preds.to_csv(RES/'holdout_predictions.csv',index=False)
    plt.figure(figsize=(6,5));plt.scatter(preds.actual_mbps,preds['Linear regression'],s=18,alpha=.55);lo=min(preds.actual_mbps.min(),preds['Linear regression'].min());hi=max(preds.actual_mbps.max(),preds['Linear regression'].max());plt.plot([lo,hi],[lo,hi],color='black');plt.xlabel('Observed download (Mbps)');plt.ylabel('Linear model prediction (Mbps)');fig('predicted_vs_observed.png')
    return scores

def cluster(df,frame):
    features=['download_mbps','upload_mbps','latency_ms','station_density','population_density']
    raw=df[features].copy()
    for c in features:raw[c]=np.log1p(raw[c])
    z=StandardScaler().fit_transform(raw);scores=[];fits={}
    for k in range(2,7):
        km=KMeans(n_clusters=k,random_state=SEED,n_init=20).fit(z);fits[k]=km
        sil=silhouette_score(z,km.labels_,sample_size=min(len(z),1500),random_state=SEED)
        scores.append({'k':k,'silhouette':sil,'inertia':km.inertia_})
    table=pd.DataFrame(scores);best=int(table.loc[table.silhouette.idxmax(),'k']);km=fits[best]
    ari=[]
    for seed in range(5):ari.append(adjusted_rand_score(km.labels_,KMeans(n_clusters=best,n_init=10,random_state=seed).fit_predict(z)))
    df=df.copy();df['cluster']=km.labels_+1
    table.to_csv(RES/'kmeans_selection.csv',index=False)
    df.groupby('cluster')[features].median().to_csv(RES/'cluster_profiles.csv')
    pd.crosstab(df.cluster,df.municipality_type).to_csv(RES/'cluster_type_crosstab.csv')
    df[['bfs_id','cluster']].to_csv(OUT/'clusters.csv',index=False)
    save_json('cluster_stability.json',{'selected_k':best,'mean_adjusted_rand':np.mean(ari),'seeds':list(range(5)),'note':'Exploratory profiles; speed included, therefore clusters do not independently validate a speed gap.'})
    plt.figure(figsize=(7,4));plt.plot(table.k,table.silhouette,'o-',color=COLORS[0]);plt.xlabel('k');plt.ylabel('Silhouette score');fig('kmeans_selection.png')
    ax=frame.merge(df[['bfs_id','cluster']],on='bfs_id',how='left',validate='one_to_one').plot(column='cluster',categorical=True,legend=True,figsize=(10,6),cmap='Set2',missing_kwds={'color':'#dddddd'},linewidth=0)
    ax.set_axis_off();ax.set_title('Exploratory network profiles | k-means\nGrey = municipality not included in modelling sample');fig('clusters_map.png')
    return best

def main():
    OUT.mkdir(parents=True,exist_ok=True);RES.mkdir(parents=True,exist_ok=True)
    print('Integrating actual source data',flush=True);frame,points=integrate()
    print('EDA',flush=True);df,groups,coverage=describe(frame,points)
    print('Inference and sensitivity',flush=True);models,gap=infer(df,frame)
    print('Held-out model comparison',flush=True);scores=predict(df)
    print('Clustering',flush=True);k=cluster(df,frame)
    save_json('summary.json',{'all_municipalities':len(frame),'observed_municipalities':int(frame.observed.sum()),'eligible_municipalities':len(df),'assigned_tiles':len(points),'tests':int(points.tests.sum()),'groups':groups.reset_index().to_dict('records'),'coverage':coverage.reset_index().to_dict('records'),'models':scores.to_dict('records'),'bootstrap':gap,'clusters':k,'infrastructure_r2_in_sample_log':models['infrastructure'].rsquared,'controls_r2_in_sample_log':models['controls'].rsquared})
    print((RES/'summary.json').read_text(),flush=True)

if __name__=='__main__':main()
