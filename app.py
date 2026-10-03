import streamlit as st
import json, random
from pathlib import Path

st.set_page_config(page_title="FisioInmune IA", layout="wide", initial_sidebar_state="collapsed")

st.markdown(r"""
<style>
.stApp{background:radial-gradient(circle at 15% 10%,rgba(219,234,254,.80),transparent 30%),radial-gradient(circle at 90% 8%,rgba(224,242,254,.68),transparent 26%),linear-gradient(180deg,#f8fbff 0%,#eef5fb 100%)}
.block-container{max-width:1080px;padding-top:3.1rem!important;padding-bottom:2.2rem!important}
.custom-header-title{display:block;color:#1f2937;font-size:1.65rem;font-weight:750;line-height:1.1;margin:0 0 3px 0}.custom-header-sub{display:block;color:#667085;font-size:.78rem;margin:0 0 5px 0}
p,label,.stMarkdown{font-size:.88rem}.stCaption{font-size:.72rem!important;margin-top:0!important}
.stButton>button{min-height:36px!important;border-radius:9px!important;font-size:.84rem!important;padding:.25rem .55rem!important}
div[data-testid="stPopover"] button{background:#eef4fa!important;color:#334155!important;border:1px solid #b9c9db!important;font-weight:650!important;min-height:34px!important;font-size:.78rem!important}
div[data-testid="stPopover"] button p,div[data-testid="stPopover"] button span{color:#334155!important}
div[role="radiogroup"]{gap:.08rem!important}div[role="radiogroup"] label{padding:.22rem .15rem!important;margin:0!important;min-height:30px!important}div[role="radiogroup"] p{font-size:.84rem!important;line-height:1.18!important;margin:0!important}
.status-row{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px;margin:.2rem 0 .25rem}.status-card{background:linear-gradient(180deg,#dceaf7,#d5e4f2);border:1px solid #b8cadc;border-radius:8px;padding:4px 6px;text-align:center;min-height:40px}.status-label{color:#5d6b7c;font-size:.60rem}.status-value{color:#23364b;font-size:.84rem;font-weight:700}
.feedback-error{border-left:3px solid #c2410c;background:#fff7ed;border-radius:7px;padding:8px 10px;margin-top:.35rem;font-size:.80rem;line-height:1.25}.feedback-ok{border-left:3px solid #15803d;background:#f0fdf4;border-radius:7px;padding:8px 10px;margin-top:.35rem;font-size:.80rem;line-height:1.25}.feedback-label{font-weight:700;color:#344054}
.fixed-footer{position:fixed!important;left:0!important;right:0!important;bottom:0!important;z-index:9999!important;background:rgba(241,247,252,.97)!important;border-top:1px solid #cad6e3!important;text-align:center!important;padding:5px 8px!important;font-size:.68rem!important;color:#5f6c7b!important}
@media(max-width:700px){.block-container{padding-top:2.6rem!important;padding-left:.45rem!important;padding-right:.45rem!important;padding-bottom:2rem!important}.custom-header-title{font-size:1.28rem}.custom-header-sub{font-size:.70rem}p,label,.stMarkdown{font-size:.80rem}.status-row{gap:4px}.status-card{padding:3px;min-height:36px}.status-label{font-size:.55rem}.status-value{font-size:.78rem}.stButton>button{min-height:34px!important;font-size:.80rem!important}div[role="radiogroup"] label{padding:.18rem .08rem!important;min-height:28px!important}div[role="radiogroup"] p{font-size:.78rem!important}.feedback-error,.feedback-ok{font-size:.76rem;padding:7px 8px}.fixed-footer{font-size:.60rem!important;padding:4px 5px!important}}
</style>
""", unsafe_allow_html=True)

PREGUNTAS=json.load(open(Path(__file__).with_name("preguntas_inmune.json"),encoding="utf-8"))
POR_ID={q["id"]:q for q in PREGUNTAS}; POR_NIVEL={n:[q for q in PREGUNTAS if q["nivel"]==n] for n in range(1,5)}; TOTAL=10

def footer(): st.markdown('<div class="fixed-footer">Creado por <strong>Cristian Barahona Videla</strong> · Uso educativo · © 2026</div>',unsafe_allow_html=True)
def init():
 d={"iniciada":False,"nombre":"","respondidas":0,"aciertos":0,"errores":0,"nivel_actual":1,"intento":1,"bloqueada":False,"feedback":"","feedback_tipo":"","actual_id":None,"historial":[],"usadas_global":set(),"usadas_sesion":set(),"orden_opciones":[]}
 for k,v in d.items():
  if k not in st.session_state: st.session_state[k]=v
def reset(mantener=True):
 nombre=st.session_state.get("nombre",""); usadas=set(st.session_state.get("usadas_global",set())) if mantener else set()
 for k in list(st.session_state.keys()): del st.session_state[k]
 init(); st.session_state.nombre=nombre; st.session_state.usadas_global=usadas
def elegir(nivel):
 cand=[q for q in POR_NIVEL[nivel] if q["id"] not in st.session_state.usadas_global]
 if not cand: cand=[q for q in PREGUNTAS if q["id"] not in st.session_state.usadas_global]
 if not cand: st.session_state.usadas_global=set(); cand=POR_NIVEL[nivel][:]
 q=random.choice(cand); st.session_state.usadas_global.add(q["id"]); st.session_state.usadas_sesion.add(q["id"]); return q["id"]
def barajar(q):
 ops=list(q["alternativas"]); random.shuffle(ops); st.session_state.orden_opciones=ops
def cargar(nivel):
 st.session_state.actual_id=elegir(nivel); barajar(POR_ID[st.session_state.actual_id])
def subir(acierto): st.session_state.nivel_actual=min(4,st.session_state.nivel_actual+1) if acierto else max(1,st.session_state.nivel_actual-1)
def iniciar(): reset(True); cargar(1); st.session_state.iniciada=True
init()

a,b=st.columns([5.6,1.3],vertical_alignment="top")
with a: st.markdown('<div class="custom-header-title">FisioInmune IA</div><div class="custom-header-sub">10 preguntas por sesión · banco de 80 preguntas · dificultad adaptativa</div>',unsafe_allow_html=True)
with b:
 if st.session_state.iniciada:
  with st.popover("↻ Reiniciar",use_container_width=True):
   st.warning("Se perderá el avance de esta sesión.")
   if st.button("Confirmar reinicio",use_container_width=True): reset(True); st.session_state.iniciada=False; st.rerun()
if not st.session_state.iniciada:
 st.markdown("**Cómo funciona**  \n10 preguntas · 4 niveles · 2 intentos · preguntas aleatorias · alternativas reordenadas también en el segundo intento · progresión adaptativa.")
 nombre=st.text_input("Nombre o nickname",value=st.session_state.nombre)
 if st.button("Comenzar sesión",use_container_width=True,type="primary"):
  if nombre.strip(): st.session_state.nombre=nombre.strip(); iniciar(); st.rerun()
  else: st.warning("Ingresa un nombre o nickname.")
 footer(); st.stop()
if st.session_state.respondidas>=TOTAL:
 st.success(f"Sesión completada, {st.session_state.nombre}."); pct=round(st.session_state.aciertos/TOTAL*100)
 c1,c2,c3,c4=st.columns(4); c1.metric("Aciertos",f"{st.session_state.aciertos}/{TOTAL}"); c2.metric("Errores",st.session_state.errores); c3.metric("Resultado",f"{pct}%"); c4.metric("Nivel máx.",max([h["nivel"] for h in st.session_state.historial] or [1]))
 with st.expander("Resumen de la sesión"):
  for i,h in enumerate(st.session_state.historial,1): st.write(f"{i}. {'✓' if h['correcta'] else '✗'} · Nivel {h['nivel']} · {h['tema']}")
 if st.button("Nueva sesión sin repetir",use_container_width=True,type="primary"): iniciar(); st.rerun()
 footer(); st.stop()
q=POR_ID[st.session_state.actual_id]
st.markdown(f'<div class="status-row"><div class="status-card"><div class="status-label">Pregunta</div><div class="status-value">{st.session_state.respondidas+1}/{TOTAL}</div></div><div class="status-card"><div class="status-label">Nivel</div><div class="status-value">{q["nivel"]}</div></div><div class="status-card"><div class="status-label">Intento</div><div class="status-value">{st.session_state.intento}/2</div></div><div class="status-card"><div class="status-label">Sin repetir</div><div class="status-value">{len(st.session_state.usadas_global)}</div></div></div>',unsafe_allow_html=True)
st.progress(st.session_state.respondidas/TOTAL)
left,right=st.columns([5.2,1.35],gap="small")
with left:
 with st.container(border=True):
  st.caption(f"Tema: {q['tema']}"); st.markdown(f"**{q['pregunta']}**")
  ops=st.session_state.orden_opciones; letras=["A","B","C","D"]; muestra=[f"{letras[i]}. {x}" for i,x in enumerate(ops)]
  sel=st.radio("Selecciona una alternativa:",muestra,index=None,key=f"radio_{q['id']}_{st.session_state.intento}",disabled=st.session_state.bloqueada)
 if st.session_state.feedback:
  clase="feedback-ok" if st.session_state.feedback_tipo=="ok" else "feedback-error"; st.markdown(f'<div class="{clase}">{st.session_state.feedback}</div>',unsafe_allow_html=True)
with right:
 if not st.session_state.bloqueada:
  responder=st.button("Responder",use_container_width=True,type="primary",disabled=(sel is None))
  if st.session_state.intento==2: st.caption("2.º intento · alternativas reordenadas")
 else:
  responder=False
  if st.button("Avanzar →",use_container_width=True,type="primary"):
   cargar(st.session_state.nivel_actual); st.session_state.intento=1; st.session_state.bloqueada=False; st.session_state.feedback=""; st.session_state.feedback_tipo=""; st.rerun()
if responder:
 elegido=ops[muestra.index(sel)]; correcta=elegido==q["correcta_texto"]
 if correcta:
  st.session_state.aciertos+=1; st.session_state.respondidas+=1; st.session_state.bloqueada=True; st.session_state.feedback_tipo="ok"; st.session_state.feedback='<span class="feedback-label">Correcto.</span><br><br><span class="feedback-label">Idea clave:</span> '+q["ideaClave"]; st.session_state.historial.append({"id":q["id"],"nivel":q["nivel"],"tema":q["tema"],"correcta":True}); subir(True)
 else:
  st.session_state.errores+=1
  if st.session_state.intento==1:
   st.session_state.intento=2; st.session_state.feedback_tipo="error"; st.session_state.feedback='<span class="feedback-label">Error porque:</span> '+q["errorComun"]+'<br><br><span class="feedback-label">Tienes un segundo intento.</span>'; barajar(q)
  else:
   st.session_state.respondidas+=1; st.session_state.bloqueada=True; st.session_state.feedback_tipo="error"; st.session_state.feedback='<span class="feedback-label">Error porque:</span> '+q["errorComun"]+'<br><br><span class="feedback-label">Respuesta correcta:</span> '+q["correcta_texto"]+'<br><br><span class="feedback-label">Idea clave:</span> '+q["ideaClave"]; st.session_state.historial.append({"id":q["id"],"nivel":q["nivel"],"tema":q["tema"],"correcta":False}); subir(False)
 st.rerun()
footer()
