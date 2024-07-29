select stks.symbol, gf.quant as gurufocus, ts.quant as thestreet, z.quant as zacks, st.quant as stocktwits, ((gf.quant+ts.quant+z.quant+st.quant)/4) as quant_avg
FROM stocks stks
JOIN gurufocus gf ON gf.symbol = stks.symbol
JOIN thestreet ts ON ts.symbol = stks.symbol
JOIN zacks z ON z.symbol = stks.symbol
JOIN stocktwits st ON st.symbol = stks.symbol
WHERE stks.symbol in ('ALSN','ALV','AMR','ANF','AOS','AYI','BCC','BLDR','BRC','CASY','CCS','CNO','COR','CSL','DJT','DVA','EHC','EME','ET','FHI','FIX','FN','GPK','GRBK','GWW','HII','HNI','HUBB','IDCC','INGR','KFY','LECO','LRN','LW','MA','MANH','META','METC','MUSA','OMC','PCAR','PERI','PFGC','PGR','PGTI','PH','POST','QCOM','QLYS','R','RL','RDY','RSG','RUM','SANM','SFM','STLD','STRL','TEL','TM','TOL','TT','TPX','TXT','UHS','VCTR','WRB','WSO')
ORDER BY quant_avg desc;
