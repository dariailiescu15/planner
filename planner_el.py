import streamlit as st
import datetime
import uuid
import json
import os

# Fișierul separat pentru el (ca să nu se amestece cu task-urile tale roz!)
FILE_NAME = "tasks_el.json"

# --- FUNCȚII PENTRU SALVARE ȘI ÎNCĂRCARE ---
def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            try:
                tasks = json.load(f)
                for task in tasks:
                    task["date"] = datetime.datetime.strptime(task["date"], "%Y-%m-%d").date()
                return tasks
            except json.JSONDecodeError:
                return []
    return[]

def save_tasks(tasks):
    tasks_to_save =[]
    for task in tasks:
        t_copy = task.copy()
        t_copy["date"] = t_copy["date"].strftime("%Y-%m-%d")
        tasks_to_save.append(t_copy)
        
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(tasks_to_save, f, indent=4)

# Setăm titlul și iconița paginii
st.set_page_config(page_title="Planner Obiective", page_icon="🎯", layout="centered")

# CSS pentru o temă modernă, dark și roșie (masculină/tactică)
st.markdown("""
    <style>
    /* Fundalul aplicației (Dark Mode) */
    .stApp { 
        background-color: #121212; 
    }
    
    /* Titlurile */
    h1, h2, h3 { 
        color: #E53935 !important; /* Roșu aprins */
        font-family: 'Helvetica Neue', Arial, sans-serif; 
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Text general */
    p { color: #E0E0E0; }
    
    /* Butoanele */
    .stButton>button { 
        background-color: #B71C1C; /* Roșu închis */
        color: white; 
        border-radius: 5px; 
        border: 1px solid #7F0000; 
        font-weight: bold; 
        text-transform: uppercase;
    }
    .stButton>button:hover { 
        background-color: #E53935; /* Roșu mai deschis la hover */
        color: white; 
        border: 1px solid #FFCDD2;
        box-shadow: 0 0 8px rgba(229, 57, 53, 0.6);
    }
    
    /* Input-uri */
    .stTextInput>div>div>input, .stDateInput>div>div>input { 
        border: 1px solid #424242; 
        border-radius: 5px; 
        background-color: #1E1E1E;
        color: white;
    }
    
    /* Caseta de bifare (Checkbox) text */
    div[data-baseweb="checkbox"] label {
        color: #FFFFFF !important;
        font-weight: 500;
    }
    div[data-baseweb="checkbox"] > div { 
        background-color: transparent; 
    }
    
    /* Stilizare carduri task-uri */
    .task-box { 
        background-color: #1E1E1E; /* Gri foarte închis */
        padding: 15px; 
        border-radius: 5px; 
        border-left: 5px solid #E53935; /* Bordură roșie */
        box-shadow: 2px 2px 10px rgba(0,0,0,0.5); 
        margin-bottom: 10px; 
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Inițializăm lista de task-uri
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

# --- TITLUL APLICAȚIEI ---
st.title("🎯 Planner ")
st.write("Planifică-ți ziua și atinge-ți obiectivele. No excuses.")

# --- SECȚIUNEA DE ADĂUGARE TASK ---
with st.container():
    st.subheader("🛠️ Adaugă task")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        task_date = st.date_input("Data:", datetime.date.today())
    with col2:
        task_desc = st.text_input("Obiectiv / Task:")
        
    if st.button("➕ Adaugă"):
        if task_desc.strip() == "":
            st.warning("Introdu un task valid!")
        else:
            new_task = {
                "id": str(uuid.uuid4()),
                "date": task_date,
                "task": task_desc,
                "done": False
            }
            st.session_state.tasks.append(new_task)
            save_tasks(st.session_state.tasks)
            st.success("Obiectiv adăugat!")
            st.rerun()

st.divider()

# --- SECȚIUNEA DE AFIȘARE TASK-URI ---
st.subheader("🔥 Obiective Active")

if len(st.session_state.tasks) == 0:
    st.info("Niciun obiectiv adăugat. Ai rezolvat tot! 🍻")
else:
    sorted_tasks = sorted(st.session_state.tasks, key=lambda x: x["date"])
    
    for task in sorted_tasks:
        st.markdown('<div class="task-box">', unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns([1, 3, 1])
        
        with c1:
            st.write(f"📅 **{task['date'].strftime('%d.%m.%Y')}**")
            
        with c2:
            is_done = st.checkbox(task["task"], value=task["done"], key=f"check_{task['id']}")
            
            if is_done != task["done"]:
                for t in st.session_state.tasks:
                    if t["id"] == task["id"]:
                        t["done"] = is_done
                save_tasks(st.session_state.tasks)
                st.rerun()
                
        with c3:
            if st.button("❌ Șterge", key=f"del_{task['id']}"):
                st.session_state.tasks =[t for t in st.session_state.tasks if t["id"] != task["id"]]
                save_tasks(st.session_state.tasks)
                st.rerun()
                
        st.markdown('</div>', unsafe_allow_html=True)
