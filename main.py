import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar, DateEntry
import threading
import schedule
import time
import os
import sys
from datetime import datetime, timedelta
from PIL import Image, ImageTk
import customtkinter as ctk  # Biblioteca de UI moderna

# Importando o script de automação
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from auto_02 import main as executar_automacao

# Configurar aparência e tema do customtkinter
ctk.set_appearance_mode("system")  # Opções: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Opções: "blue", "green", "dark-blue"

class AutomacaoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Automação de Cotações de Frete Logdi")
        self.root.geometry("900x650")
        self.root.minsize(800, 600)
        
        # Variáveis
        self.agendamento_ativo = False
        self.thread_agendamento = None
        self.horario_var = tk.StringVar(value="08:00")
        self.frequencia_var = tk.StringVar(value="Diariamente")
        self.status_var = tk.StringVar(value="Pronto")

        # Esquema de cores
        self.colors = {
            "primary": "#1E88E5",       # Azul
            "primary_dark": "#1565C0",   # Azul mais escuro
            "secondary": "#4CAF50",     # Verde
            "danger": "#E53935",        # Vermelho
            "text": "#212121",          # Cinza escuro para texto
            "text_secondary": "#757575", # Cinza médio para texto menos importante
            "background": "#F5F5F5",    # Fundo cinza claro
            "card": "#FFFFFF",          # Branco para cards
            "border": "#E0E0E0"         # Cinza claro para bordas
        }
        
        # Criar e organizar widgets
        self.create_widgets()
    
    def create_widgets(self):
        # Container principal
        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Cabeçalho com logo e título
        self.create_header()
        
        # Área de conteúdo com barra lateral e conteúdo principal
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Criar barra lateral
        self.create_sidebar()
        
        # Criar área de conteúdo principal
        self.create_main_content()
        
        # Criar rodapé
        self.create_footer()

    def create_header(self):
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent", height=60)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Tentar carregar logo
        try:
            logo_img = Image.open("logo.png")
            logo_img = logo_img.resize((40, 40), Image.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = ctk.CTkLabel(header_frame, image=logo_photo, text="")
            logo_label.image = logo_photo
            logo_label.pack(side=tk.LEFT, padx=(0, 10))
        except:
            # Se o logo não puder ser carregado, usar um espaço reservado
            logo_label = ctk.CTkLabel(header_frame, text="🚚", font=ctk.CTkFont(size=24, weight="bold"))
            logo_label.pack(side=tk.LEFT, padx=(0, 10))
        
        title_label = ctk.CTkLabel(
            header_frame, 
            text="Automação de Cotações de Frete", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(side=tk.LEFT)
        
        # Indicador de status
        status_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        status_frame.pack(side=tk.RIGHT)
        
        status_indicator = ctk.CTkLabel(
            status_frame,
            text="●",
            font=ctk.CTkFont(size=16),
            text_color="#4CAF50"  # Ponto verde para status
        )
        status_indicator.pack(side=tk.LEFT, padx=(0, 5))
        
        self.status_label = ctk.CTkLabel(
            status_frame, 
            textvariable=self.status_var,
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(side=tk.LEFT)

    def create_sidebar(self):
        # Barra lateral
        self.sidebar = ctk.CTkFrame(self.content_frame, width=250, corner_radius=10)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        
        # Fazer a barra lateral manter sua largura
        self.sidebar.pack_propagate(False)
        
        # Cabeçalho de opções
        options_label = ctk.CTkLabel(
            self.sidebar,
            text="Configurações",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        options_label.pack(fill=tk.X, padx=20, pady=(20, 15))
        
        # Configurações de tempo
        time_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        time_frame.pack(fill=tk.X, padx=20, pady=10)
        
        time_label = ctk.CTkLabel(
            time_frame, 
            text="Horário de Execução:",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        time_label.pack(fill=tk.X)
        
        time_selector = ctk.CTkFrame(time_frame, fg_color="transparent")
        time_selector.pack(fill=tk.X, pady=(5, 0))
        
        # Seleção de hora
        horas = [f"{h:02d}" for h in range(24)]
        self.hora_combo = ctk.CTkOptionMenu(
            time_selector,
            values=horas,
            width=80
        )
        self.hora_combo.set("08")
        self.hora_combo.pack(side=tk.LEFT)
        
        separator_label = ctk.CTkLabel(time_selector, text=":", font=ctk.CTkFont(size=16, weight="bold"))
        separator_label.pack(side=tk.LEFT, padx=5)
        
        # Seleção de minuto
        minutos = [f"{m:02d}" for m in range(0, 60, 5)]
        self.minuto_combo = ctk.CTkOptionMenu(
            time_selector,
            values=minutos,
            width=80
        )
        self.minuto_combo.set("00")
        self.minuto_combo.pack(side=tk.LEFT)
        
        # Configurações de frequência
        freq_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        freq_frame.pack(fill=tk.X, padx=20, pady=10)
        
        freq_label = ctk.CTkLabel(
            freq_frame, 
            text="Frequência:",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        freq_label.pack(fill=tk.X)
        
        frequencias = ["Diariamente", "Semanalmente", "Uma vez"]
        self.freq_combo = ctk.CTkOptionMenu(
            freq_frame,
            values=frequencias,
            command=self.on_frequencia_change,
            width=200
        )
        self.freq_combo.set("Diariamente")
        self.freq_combo.pack(fill=tk.X, pady=(5, 0))
        
        # Seleção de dia da semana (inicialmente oculta)
        self.dia_semana_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        
        dia_semana_label = ctk.CTkLabel(
            self.dia_semana_frame, 
            text="Dia da Semana:",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        dia_semana_label.pack(fill=tk.X)
        
        dias_semana = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
        self.dia_semana_combo = ctk.CTkOptionMenu(
            self.dia_semana_frame,
            values=dias_semana,
            width=200
        )
        self.dia_semana_combo.set("Segunda-feira")
        self.dia_semana_combo.pack(fill=tk.X, pady=(5, 0))
        
        # Seleção de data específica (inicialmente oculta)
        self.data_especifica_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        
        data_label = ctk.CTkLabel(
            self.data_especifica_frame, 
            text="Data Específica:",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        data_label.pack(fill=tk.X)
        
        # Seletor de data será colocado em um sub-frame para evitar conflitos visuais
        date_picker_frame = tk.Frame(self.data_especifica_frame, bg=self.root.cget("bg"))
        date_picker_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.data_entry = DateEntry(
            date_picker_frame, 
            width=12, 
            background=self.colors["primary"],
            foreground='white', 
            borderwidth=0,
            date_pattern='dd/mm/yyyy'
        )
        self.data_entry.pack(fill=tk.X)
        
        # Botões de ação na parte inferior da barra lateral
        self.create_action_buttons()

    def create_action_buttons(self):
        # Separador
        separator = ctk.CTkFrame(self.sidebar, height=1, fg_color=self.colors["border"])
        separator.pack(fill=tk.X, padx=20, pady=20)
        
        # Botões de ação
        buttons_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        buttons_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Botão de agendar
        self.agendar_btn = ctk.CTkButton(
            buttons_frame, 
            text="Agendar Automação",
            font=ctk.CTkFont(size=13, weight="bold"),
            height=38,
            corner_radius=8,
            command=self.agendar_automacao
        )
        self.agendar_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Botão de cancelar
        self.cancelar_btn = ctk.CTkButton(
            buttons_frame, 
            text="Cancelar Agendamento",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=self.colors["danger"],
            hover_color="#C62828",  # Vermelho mais escuro
            height=38,
            corner_radius=8,
            command=self.cancelar_agendamento
        )
        self.cancelar_btn.pack(fill=tk.X, pady=(0, 10))
        self.cancelar_btn.configure(state="disabled")
        
        # Botão de executar agora
        self.executar_agora_btn = ctk.CTkButton(
            buttons_frame, 
            text="Executar Agora",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=self.colors["secondary"],
            hover_color="#388E3C",  # Verde mais escuro
            height=38,
            corner_radius=8,
            command=self.executar_agora
        )
        self.executar_agora_btn.pack(fill=tk.X)

    def create_main_content(self):
        # Área de conteúdo principal
        self.main_content = ctk.CTkFrame(self.content_frame, corner_radius=10)
        self.main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Painel de informações com animação
        info_frame = ctk.CTkFrame(self.main_content, fg_color=self.colors["primary"], corner_radius=8)
        info_frame.pack(fill=tk.X, padx=20, pady=20)
        
        info_content = ctk.CTkFrame(info_frame, fg_color="transparent")
        info_content.pack(padx=20, pady=20)
        
        # Ícone de informação
        info_icon = ctk.CTkLabel(
            info_content, 
            text="ℹ️",
            font=ctk.CTkFont(size=24),
            text_color="white"
        )
        info_icon.pack(anchor=tk.W)
        
        info_title = ctk.CTkLabel(
            info_content, 
            text="Coleta Automatizada de Cotações de Frete",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white"
        )
        info_title.pack(anchor=tk.W, pady=(5, 10))
        
        info_text = ctk.CTkLabel(
            info_content, 
            text="Esta aplicação automatiza o processo de coleta de dados de cotações de frete.\n"
                 "Agende quando deseja que a automação seja executada usando as opções na barra lateral.",
            font=ctk.CTkFont(size=12),
            text_color="white",
            justify=tk.LEFT
        )
        info_text.pack(anchor=tk.W)
        
        # Área de log
        log_frame = ctk.CTkFrame(self.main_content)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        log_header = ctk.CTkFrame(log_frame, fg_color="transparent", height=40)
        log_header.pack(fill=tk.X, padx=15, pady=(15, 0))
        
        log_title = ctk.CTkLabel(
            log_header, 
            text="Log de Execução",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        log_title.pack(side=tk.LEFT)
        
        # Informações da última execução
        self.last_execution_label = ctk.CTkLabel(
            log_header, 
            text="Última execução: Nunca",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_secondary"]
        )
        self.last_execution_label.pack(side=tk.RIGHT)
        
        # Área de texto do log com estilo personalizado
        log_container = ctk.CTkFrame(log_frame, fg_color="transparent")
        log_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self.log_text = tk.Text(
            log_container, 
            height=10, 
            width=80, 
            wrap=tk.WORD,
            bg="#FFFFFF",
            fg=self.colors["text"],
            font=("Consolas", 10),
            borderwidth=0,
            padx=10,
            pady=10
        )
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ctk.CTkScrollbar(log_container, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text.configure(yscrollcommand=scrollbar.set)
        self.log_text.config(state=tk.DISABLED)
        
        # Adicionar mensagem inicial ao log
        self.adicionar_log("Sistema inicializado e pronto.")

    def create_footer(self):
        footer_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent", height=30)
        footer_frame.pack(fill=tk.X, pady=(10, 0))
        
        footer_text = ctk.CTkLabel(
            footer_frame, 
            text="© 2025 Logdi - Todos os direitos reservados",
            font=ctk.CTkFont(size=10),
            text_color=self.colors["text_secondary"]
        )
        footer_text.pack(side=tk.RIGHT)
        
        # Informação de versão
        version_text = ctk.CTkLabel(
            footer_frame, 
            text="v2.0",
            font=ctk.CTkFont(size=10),
            text_color=self.colors["text_secondary"]
        )
        version_text.pack(side=tk.LEFT)

    def on_frequencia_change(self, choice):
        # Ocultar todos os frames adicionais
        self.dia_semana_frame.pack_forget()
        self.data_especifica_frame.pack_forget()
        
        # Mostrar o frame apropriado com base na seleção
        if choice == "Semanalmente":
            self.dia_semana_frame.pack(fill=tk.X, padx=20, pady=10)
        elif choice == "Uma vez":
            self.data_especifica_frame.pack(fill=tk.X, padx=20, pady=10)
    
    def adicionar_log(self, mensagem):
        """Adiciona uma mensagem ao log de execução."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"[{timestamp}] {mensagem}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def executar_agora(self):
        """Executa a automação imediatamente."""
        self.adicionar_log("Iniciando execução da automação...")
        threading.Thread(target=self.executar_automacao_thread).start()
    
    def executar_automacao_thread(self):
        """Executa a automação em uma thread separada."""
        try:
            self.status_var.set("Executando...")
            self.agendar_btn.configure(state="disabled")
            self.executar_agora_btn.configure(state="disabled")
            
            # Executar automação
            executar_automacao()
            
            now = datetime.now().strftime("%d/%m/%Y %H:%M")
            self.adicionar_log("Automação concluída com sucesso!")
            self.status_var.set("Pronto")
            self.last_execution_label.configure(text=f"Última execução: {now}")
        except Exception as e:
            self.adicionar_log(f"Erro durante a automação: {str(e)}")
            self.status_var.set("Erro!")
            messagebox.showerror("Erro", f"Ocorreu um erro durante a execução: {str(e)}")
        finally:
            self.agendar_btn.configure(state="normal")
            self.executar_agora_btn.configure(state="normal")
    
    def agendar_automacao(self):
        """Agenda a execução da automação com base nas configurações selecionadas."""
        if self.agendamento_ativo:
            messagebox.showinfo("Aviso", "Já existe um agendamento ativo. Cancele-o primeiro.")
            return
        
        # Obter horário configurado
        hora = self.hora_combo.get()
        minuto = self.minuto_combo.get()
        horario = f"{hora}:{minuto}"
        
        # Configurar o agendamento de acordo com a frequência
        frequencia = self.freq_combo.get()
        
        if frequencia == "Diariamente":
            descricao = f"Agendado para executar diariamente às {horario}"
        elif frequencia == "Semanalmente":
            dia_semana = self.dia_semana_combo.get()
            descricao = f"Agendado para executar toda(o) {dia_semana} às {horario}"
        else:  # Uma vez
            data = self.data_entry.get_date().strftime("%d/%m/%Y")
            descricao = f"Agendado para executar em {data} às {horario}"
        
        # Iniciar thread de agendamento
        self.agendamento_ativo = True
        self.thread_agendamento = threading.Thread(target=self.monitorar_agendamento, 
                                                  args=(horario, frequencia))
        self.thread_agendamento.daemon = True
        self.thread_agendamento.start()
        
        # Atualizar interface
        self.status_var.set("Agendamento ativo")
        self.agendar_btn.configure(state="disabled")
        self.cancelar_btn.configure(state="normal")
        self.adicionar_log(descricao)
        
        messagebox.showinfo("Agendamento", descricao)
    
    def cancelar_agendamento(self):
        """Cancela o agendamento atual."""
        if not self.agendamento_ativo:
            return
        
        schedule.clear()
        self.agendamento_ativo = False
        
        # Atualizar interface
        self.status_var.set("Pronto")
        self.agendar_btn.configure(state="normal")
        self.cancelar_btn.configure(state="disabled")
        self.adicionar_log("Agendamento cancelado")
        
        messagebox.showinfo("Cancelamento", "Agendamento cancelado com sucesso.")
    
    def monitorar_agendamento(self, horario, frequencia):
        """Monitora o agendamento e executa a automação quando for a hora."""
        # Limpar agendamentos anteriores
        schedule.clear()
        
        # Configurar novo agendamento com base na frequência
        if frequencia == "Diariamente":
            schedule.every().day.at(horario).do(self.executar_automacao_thread)
        elif frequencia == "Semanalmente":
            dia_semana = self.dia_semana_combo.get().lower()
            if dia_semana == "segunda-feira":
                schedule.every().monday.at(horario).do(self.executar_automacao_thread)
            elif dia_semana == "terça-feira":
                schedule.every().tuesday.at(horario).do(self.executar_automacao_thread)
            elif dia_semana == "quarta-feira":
                schedule.every().wednesday.at(horario).do(self.executar_automacao_thread)
            elif dia_semana == "quinta-feira":
                schedule.every().thursday.at(horario).do(self.executar_automacao_thread)
            elif dia_semana == "sexta-feira":
                schedule.every().friday.at(horario).do(self.executar_automacao_thread)
            elif dia_semana == "sábado":
                schedule.every().saturday.at(horario).do(self.executar_automacao_thread)
            elif dia_semana == "domingo":
                schedule.every().sunday.at(horario).do(self.executar_automacao_thread)
        else:  # Uma vez
            data_especifica = self.data_entry.get_date()
            data_hora_especifica = datetime.combine(data_especifica, 
                                                  datetime.strptime(horario, "%H:%M").time())
            
            # Para data específica, verificar se o horário já passou
            if data_hora_especifica < datetime.now():
                self.root.after(0, lambda: messagebox.showwarning("Aviso", 
                               "A data/hora especificada já passou. Agendamento cancelado."))
                self.root.after(0, self.cancelar_agendamento)
                return
            
            # Schedule.every() não suporta datas específicas, então precisamos verificar manualmente
            while self.agendamento_ativo:
                now = datetime.now()
                if (now.hour == int(horario.split(":")[0]) and 
                    now.minute == int(horario.split(":")[1]) and
                    now.date() == data_especifica):
                    self.root.after(0, self.executar_automacao_thread)
                    # Após executar uma vez, cancelar o agendamento
                    self.root.after(0, self.cancelar_agendamento)
                    break
                time.sleep(30)  # Verificar a cada 30 segundos
            return
        
        # Loop de verificação de agendamento
        while self.agendamento_ativo:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    # Criar a janela principal com customtkinter
    root = ctk.CTk()
    
    # Definir ícone do aplicativo se disponível
    try:
        if os.path.exists("icon.ico"):
            root.iconbitmap("icon.ico")
    except:
        pass
    
    app = AutomacaoApp(root)
    root.mainloop()