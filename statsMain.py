# Presentacion final de estadisticas
import stats as st
import statsGUI as stg

manejo = st.ManejoInfo("resources/creds.json")
gui = stg.VerInfo(manejo)
gui.mainloop()