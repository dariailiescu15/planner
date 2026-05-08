import streamlit as st
import datetime
import uuid
import json
import os

# Numele fișierului în care se vor salva task-urile
FILE_NAME = "tasks.json"

# --- FUNCȚII PENTRU SALVARE ȘI ÎNCĂRCARE ---
def load_tasks():
    """Încarcă task-urile din fișierul JSON, dacă există."""
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            try:
                tasks = json.load(f)
                # Transformăm data din text înapoi în format 'date' pentru Streamlit
                for task in tasks:
                    task["date"] = datetime.datetime.strptime(task["date"], "%Y-%m-%d").date()
                return tasks
            except json.JSONDecodeError:
                return []
    return[]

def save_tasks(tasks):
    """Salvează lista de task-uri în fișierul JSON."""
    tasks_to_save =[]
    for task in tasks:
        # Creăm o copie pentru a transforma data în text (JSON nu suportă formatul date direct)
        t_copy = task.copy()
        t_copy["date"] = t_copy["date"].strftime("%Y-%m-%d")
        tasks_to_save.append(t_copy)
        
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(tasks_to_save, f, indent=4)

# Setăm titlul și iconița paginii
st.set_page_config(page_title="Planner Roz", page_icon="🌸", layout="centered")

# CSS pentru tema ROZ
st.markdown("""
    <style>
    .stApp { background-color: #FFF0F5; }
    h1, h2, h3 { color: #FF1493 !important; font-family: 'Comic Sans MS', cursive, sans-serif; }
    .stButton>button { background-color: #FF69B4; color: white; border-radius: 10px; border: 2px solid #FF1493; font-weight: bold; }
    .stButton>button:hover { background-color: #FF1493; color: white; border: 2px solid #C71585; }
    div[data-baseweb="checkbox"] > div { background-color: transparent; }
    .stTextInput>div>div>input, .stDateInput>div>div>input { border: 2px solid #FFB6C1; border-radius: 5px; }
    .task-box { background-color: white; padding: 15px; border-radius: 10px; border-left: 5px solid #FF69B4; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# Inițializăm lista de task-uri încărcând-o din fișier
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

# --- TITLUL APLICAȚIEI ---
st.title("🌸 Plannerul Meu Roz")
st.write("Adaugă task-urile tale și organizează-ți ziua!")

# --- SECȚIUNEA DE ADĂUGARE TASK ---
with st.container():
    st.subheader("🎀 Adaugă un task nou")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        task_date = st.date_input("Alege data:", datetime.date.today())
    with col2:
        task_desc = st.text_input("Ce ai de făcut?")
        
    if st.button("➕ Adaugă Task"):
        if task_desc.strip() == "":
            st.warning("Te rog să scrii un task!")
        else:
            new_task = {
                "id": str(uuid.uuid4()),
                "date": task_date,
                "task": task_desc,
                "done": False
            }
            st.session_state.tasks.append(new_task)
            save_tasks(st.session_state.tasks) # SALVĂM ÎN FIȘIER
            st.success("Task-ul a fost adăugat cu succes!")
            st.rerun()

st.divider()

# --- SECȚIUNEA DE AFIȘARE TASK-URI ---
st.subheader("📋 Lista ta de Task-uri")

if len(st.session_state.tasks) == 0:
    st.info("Niciun task adăugat momentan. Ești liberă! ✨")
else:
    sorted_tasks = sorted(st.session_state.tasks, key=lambda x: x["date"])
    
    for task in sorted_tasks:
        st.markdown('<div class="task-box">', unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns([1, 3, 1])
        
        with c1:
            st.write(f"📅 **{task['date'].strftime('%d.%m.%Y')}**")
            
        with c2:
            is_done = st.checkbox(task["task"], value=task["done"], key=f"check_{task['id']}")
            
            # Dacă cineva bifează/debifează, actualizăm și salvăm
            if is_done != task["done"]:
                for t in st.session_state.tasks:
                    if t["id"] == task["id"]:
                        t["done"] = is_done
                save_tasks(st.session_state.tasks) # SALVĂM ÎN FIȘIER
                st.rerun()
                
        with c3:
            if st.button("❌ Șterge", key=f"del_{task['id']}"):
                st.session_state.tasks = [t for t in st.session_state.tasks if t["id"] != task["id"]]
                save_tasks(st.session_state.tasks) # SALVĂM ÎN FIȘIER
                st.rerun()
                
        st.markdown('</div>', unsafe_allow_html=True)
