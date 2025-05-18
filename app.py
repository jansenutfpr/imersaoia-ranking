import streamlit as st
import re

def load_messages(filename="messages.txt"):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    
    messages = content.split('---')
    
    projects = []
    for message in messages:
        if not message.strip():
            continue
        
        nome_match = re.search(r'Nome: (.*?)(?:\n|$)', message)
        votos_match = re.search(r'Votos: (\d+)', message)
        link_match = re.search(r'Link:\s*(https?://\S+)', message)
        desc_match = re.search(r'Descrição: (.*?)(?:\n|$)', message, re.DOTALL)
        user_match = re.search(r'Usuário: (.*?)(?:\n|$)', message)
        
        if nome_match and votos_match and link_match:
            projects.append({
                'nome': nome_match.group(1).strip(),
                'votos': int(votos_match.group(1)),
                'link': link_match.group(1).strip(),
                'descricao': desc_match.group(1).strip() if desc_match else '',
                'usuario': user_match.group(1).strip() if user_match else ''
            })
    
    return projects
  
# Define o diálogo uma única vez
@st.dialog("Detalhes do Projeto")
def show_details():
    project = st.session_state.selected_project
    st.markdown(f"### {project['nome']}")
    st.markdown(f"**Usuário Discord:** {project['usuario']}")
    st.markdown(f"**Descrição:** {project['descricao']}")
    st.markdown(f"[Abrir no GitHub]({project['link']})")

def styles():
    st.markdown("""
            <style>
                .gradient-text {
                    background: linear-gradient(
                        to right,
                        #f8cdda,  /* rosa pastel */
                        #fbc2eb,  /* lavanda rosado */
                        #c2e9fb,  /* azul bebê */
                        #d4fc79,  /* verde-limão suave */
                        #fff6b7,  /* amarelo claro */
                        #a1c4fd,  /* azul céu */
                        #d3cce3,  /* lilás suave */
                        #fde2e4,  /* rosa-chá */
                        #f8edeb,  /* bege claro */
                        #fbc2eb,  /* repete lavanda */
                        #f8cdda   /* fecha com rosa pastel */
                    );
                    -webkit-background-clip: text;
                    background-clip: text;
                    color: transparent;
                    animation: rainbow 7s linear infinite;
                    background-size: 200% 100%;
                    font-weight: bold;
                }

                .gold-text {
                    background: linear-gradient(45deg, #FFD700, #FDB931, #F0C419);
                    -webkit-background-clip: text;
                    background-clip: text;
                    color: transparent;
                    font-weight: bold;
                    text-shadow: 0 0 10px rgba(255, 215, 0, 0.2);
                }

                .silver-text {
                    background: linear-gradient(45deg, #C0C0C0, #E8E8E8, #A8A8A8);
                    -webkit-background-clip: text;
                    background-clip: text;
                    color: transparent;
                    font-weight: bold;
                    text-shadow: 0 0 10px rgba(192, 192, 192, 0.2);
                }

                .bronze-text {
                    background: linear-gradient(45deg, #CD7F32, #B87333, #E59F54);
                    -webkit-background-clip: text;
                    background-clip: text;
                    color: transparent;
                    font-weight: bold;
                    text-shadow: 0 0 10px rgba(205, 127, 50, 0.2);
                }

                @keyframes rainbow {
                    0% { background-position: 0% 50%; }
                    100% { background-position: -200% 50%; }
                }

                @keyframes shine {
                    to {
                        background-position: 200% center;
                    }
                }

                .project-name-container {
                    min-height: 4.5em;
                    max-height: 4.5em;
                    margin-bottom: 0.5em;
                    overflow: hidden;
                    display: -webkit-box;
                    -webkit-line-clamp: 2;
                    -webkit-box-orient: vertical;
                }

                .project-name {
                    margin: 0;
                    line-height: 1.2;
                    font-size: 1.1em;
                }
                </style>
""", unsafe_allow_html=True)


def main():
    
    st.set_page_config(page_title="Projetos Imersão IA", layout="centered", initial_sidebar_state="expanded", page_icon="🏆")
    styles()
    st.title("🏆 :orange[Top Projetos] - :blue[Imersão IA]")
    st.markdown("Ranking :gray[_(não oficial)_] dos projetos mais votados da Imersão IA :blue[Alura] + **:blue[G]:red[o]:orange[o]:blue[g]:green[l]:red[e]**!")
    st.markdown("⭐ Você pode retribuir e :orange[votar] o meu [projeto](https://discord.com/channels/1369193715989614684/1369193716434337849/1373142479859355749)!")
    st.markdown("👾 Acesse o código desse :green[open-source] [aqui](https://github.com/matheusaudibert/imersaoia-ranking).")
    projects = load_messages()
    sorted_projects = sorted(projects, key=lambda x: x['votos'], reverse=True)
    
    # Pega o número de votos do 30º projeto
    min_votes = sorted_projects[29]['votos'] if len(sorted_projects) >= 30 else 0
    st.info(f"O número mínimo para estar no ranking é de :blue[**{min_votes} votos**].")
    
    st.sidebar.error("A votação se encerra às 23:59.")
    
    # Sidebar search
    st.sidebar.title("🔎 Pesquise o seu projeto!")
    search_term = st.sidebar.text_input("Digite o nome seu nome:").lower()
    

    if search_term:
        search_results = [p for p in projects if search_term in p['nome'].lower()]
        if search_results:
            for project in search_results:
                st.sidebar.markdown("---")
                st.sidebar.markdown(f"### {project['nome']}")
                st.sidebar.markdown(f"**Votos:** {project['votos']}")
                st.sidebar.markdown(f"**Usuário Discord:** {project['usuario']}")
                st.sidebar.markdown(f"**Descrição:** {project['descricao']}")
                st.sidebar.markdown(f"[Link do Projeto]({project['link']})")
        else:
            st.sidebar.warning("Nenhum projeto encontrado.")

    cols = st.columns(3)
    for idx, project in enumerate(sorted_projects[:30]):
        col = cols[idx % 3]
        with col:
            medal_class = ''
            if idx == 0:
                medal_class = 'gold-text'
            elif idx == 1:
                medal_class = 'silver-text'
            elif idx == 2:
                medal_class = 'bronze-text'

            if project['nome'] == "Matheus Audibert":
                st.markdown(
                    f"""
                    <div class="project-name-container">
                        <h5 class="project-name">{idx + 1}. <span class="gradient-text">{project['nome']}</span></h5>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            elif medal_class:
                st.markdown(
                    f"""
                    <div class="project-name-container">
                        <h5 class="project-name">{idx + 1}. <span class="{medal_class}">{project['nome']}</span></h5>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div class="project-name-container">
                        <h5 class="project-name">{idx + 1}. {project['nome']}</h5>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            st.markdown(f"**Votos:** **{project['votos']}**")
            col1, col2 = st.columns(2)
            with col1:
                st.link_button("GitHub", url=project['link'], type="primary", use_container_width=True)
            with col2:
              if st.button("Detalhes", key=f"detalhes_{idx}", use_container_width=True):
                  st.session_state.selected_project = project
                  show_details()  # Chama o dialog aqui com o projeto certo
                  
    st.write("")
    st.write("")
    st.markdown("""
    <div style='text-align: center; font-family: "Segoe UI Emoji", "Apple Color Emoji", "Noto Color Emoji", sans-serif;'>
        Feito com carinho 💙 por <a href="https://github.com/matheusaudibert" target="_blank">Matheus Audibert</a>
    </div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
