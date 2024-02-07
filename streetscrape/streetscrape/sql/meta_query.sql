select stks.symbol, gf.quant as gurufocus, ts.quant as thestreet, z.quant as zacks, st.quant as stocktwits, ((gf.quant+ts.quant+z.quant+st.quant)/4) as quant_avg
FROM stocks stks
JOIN gurufocus gf ON gf.symbol = stks.symbol
JOIN thestreet ts ON ts.symbol = stks.symbol
JOIN zacks z ON z.symbol = stks.symbol
JOIN stocktwits st ON st.symbol = stks.symbol
ORDER BY quant_avg desc;