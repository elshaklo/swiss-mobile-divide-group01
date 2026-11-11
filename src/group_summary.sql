SELECT m.municipality_type, COUNT(DISTINCT m.bfs_id) AS municipalities,
    COUNT(t.quadkey) AS tiles, SUM(t.tests) AS tests,
    SUM(t.download_mbps*t.tests)/SUM(t.tests) AS test_weighted_download_mbps
    FROM municipalities m JOIN tiles t ON m.bfs_id=t.bfs_id
    GROUP BY m.municipality_type ORDER BY m.municipality_type;
