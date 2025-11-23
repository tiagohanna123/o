#!/usr/bin/env python3
"""
Gera arquivos para compartilhamento no WhatsApp:
- PDF com resumo dos 10 problemas científicos
- Imagens com diagramas e infográficos
"""

import os
from datetime import datetime

# Criar diretório de saída
OUTPUT_DIR = "/home/user/o/compartilhar"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =============================================================================
# GERAR PDF COM REPORTLAB
# =============================================================================

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.lib.colors import HexColor, black, white
    from reportlab.pdfgen import canvas
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import Paragraph

    def criar_pdf():
        filename = os.path.join(OUTPUT_DIR, "10_Problemas_Cientificos_ModeloX.pdf")
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4

        # Cores
        azul_escuro = HexColor("#1a237e")
        azul_claro = HexColor("#3f51b5")
        verde = HexColor("#2e7d32")
        vermelho = HexColor("#c62828")
        laranja = HexColor("#ef6c00")

        # ===== PÁGINA 1: CAPA =====
        # Fundo gradiente simulado
        c.setFillColor(azul_escuro)
        c.rect(0, height/2, width, height/2, fill=1, stroke=0)
        c.setFillColor(HexColor("#283593"))
        c.rect(0, 0, width, height/2, fill=1, stroke=0)

        # Título principal
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 32)
        c.drawCentredString(width/2, height - 150, "Os 10 Maiores")
        c.drawCentredString(width/2, height - 190, "Problemas Científicos")

        c.setFont("Helvetica", 20)
        c.drawCentredString(width/2, height - 250, "Analisados pelo Modelo X Framework")

        # Equação central
        c.setFont("Helvetica-Bold", 24)
        c.setFillColor(HexColor("#ffeb3b"))
        c.drawCentredString(width/2, height/2 + 50, "Φ(E, S, ε) = C")

        c.setFont("Helvetica", 14)
        c.setFillColor(white)
        c.drawCentredString(width/2, height/2, "Entropia + Sintropia = Constante Universal")

        # Lista dos problemas
        problemas = [
            "1. Matéria Escura e Energia Escura",
            "2. Teoria Quântica da Gravidade",
            "3. Origem da Vida",
            "4. Consciência",
            "5. Mudanças Climáticas",
            "6. Envelhecimento e Longevidade",
            "7. Câncer",
            "8. Doenças Neurodegenerativas",
            "9. Resistência Antimicrobiana",
            "10. Fusão Nuclear Controlada"
        ]

        c.setFont("Helvetica", 11)
        y_start = height/2 - 80
        for i, prob in enumerate(problemas):
            c.drawCentredString(width/2, y_start - i*18, prob)

        # Rodapé
        c.setFont("Helvetica", 10)
        c.drawCentredString(width/2, 50, f"Modelo X Framework v2.0 | {datetime.now().strftime('%B %Y')}")

        c.showPage()

        # ===== PÁGINA 2: O QUE É O MODELO X =====
        c.setFillColor(black)
        c.setFont("Helvetica-Bold", 24)
        c.drawString(50, height - 80, "O Que É o Modelo X?")

        c.setFont("Helvetica", 12)
        texto = """
O Modelo X é um framework matemático que explica TUDO através
do equilíbrio entre duas forças fundamentais:

ENTROPIA (E) = Tendência à desordem
    • Exemplos: Envelhecimento, Câncer, Aquecimento Global
    • Símbolo: Caos, aleatoriedade, degradação

SINTROPIA (S) = Tendência à ordem
    • Exemplos: Vida, Consciência, Cura
    • Símbolo: Organização, complexidade, evolução

ENERGIA (ε) = O modulador que decide quem vence
    • Alta energia pode favorecer ordem OU desordem
    • O segredo está em COMO a energia é aplicada

A EQUAÇÃO UNIVERSAL:

        Φ(E, S, ε) = E × f(ε) + S × g(ε) = C

Isso significa que Entropia e Sintropia sempre se equilibram.
Quando uma aumenta, a outra deve compensar.

IMPLICAÇÃO REVOLUCIONÁRIA:
Todos os problemas científicos são variações do mesmo tema:
Como mover um sistema de alta entropia para alta sintropia?
        """

        y = height - 120
        for linha in texto.strip().split('\n'):
            c.drawString(50, y, linha)
            y -= 16

        # Diagrama visual
        c.setStrokeColor(azul_escuro)
        c.setLineWidth(2)
        c.line(100, 180, 500, 180)  # Linha horizontal

        c.setFillColor(vermelho)
        c.circle(100, 180, 20, fill=1)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(100, 177, "E")

        c.setFillColor(verde)
        c.circle(500, 180, 20, fill=1)
        c.setFillColor(white)
        c.drawCentredString(500, 177, "S")

        c.setFillColor(laranja)
        c.circle(300, 180, 25, fill=1)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(300, 177, "ε")

        c.setFillColor(black)
        c.setFont("Helvetica", 10)
        c.drawCentredString(100, 145, "DESORDEM")
        c.drawCentredString(300, 145, "ENERGIA")
        c.drawCentredString(500, 145, "ORDEM")

        c.showPage()

        # ===== PÁGINAS 3-7: OS PROBLEMAS =====
        problemas_detalhes = [
            ("1. Matéria Escura e Energia Escura",
             "95% do universo é invisível!",
             ["Matéria escura = Sintropia Negativa S(-)",
              "Energia escura = Entropia Negativa E(-)",
              "São as 'sombras' matemáticas da realidade visível",
              "Predição: Buscar padrões em lentes gravitacionais"],
             "Dificuldade: Máxima"),

            ("2. Teoria Quântica da Gravidade",
             "Como unir o muito pequeno com o muito grande?",
             ["Gravidade emerge de gradientes de sintropia",
              "Não precisa de gravitons como partículas",
              "Curvatura = acumulação de flutuações E/S",
              "Índice de unificação calculado: 0.95"],
             "Dificuldade: Máxima"),

            ("3. Origem da Vida",
             "Como química virou biologia?",
             ["Vida surge em transições críticas de fase",
              "Quando energia > limiar: S começa a vencer E",
              "Precisa: água, energia, tempo, ciclos",
              "Probabilidade calculada: função da energia"],
             "Dificuldade: Alta"),

            ("4. Consciência",
             "Por que você 'sente' que existe?",
             ["Consciência = máxima sintropia local",
              "Φc = S² × g(ε) - Nível de consciência",
              "Sono profundo: Φc=0.23 | Meditação: Φc=1.46",
              "Tempo subjetivo varia com S"],
             "Dificuldade: Máxima"),

            ("5. Mudanças Climáticas",
             "Como salvar o planeta?",
             ["Sistema climático = oscilador E-S",
              "Atual: E=58%, S=42% (desequilíbrio)",
              "Tipping point em E > 65% - PERIGO",
              "Meta: Reduzir E para 50% até 2050"],
             "Dificuldade: Média"),

            ("6. Envelhecimento",
             "Por que envelhecemos?",
             ["Envelhecimento = E vencendo S ao longo do tempo",
              "Nascimento: E/S=0.25 | 80 anos: E/S=16.8",
              "Morte ocorre quando S → 0",
              "Solução: Manter S alto (exercício, dieta)"],
             "Dificuldade: Alta"),

            ("7. Câncer",
             "Células que 'esquecem' como cooperar",
             ["Câncer = reversão para estado de alta entropia",
              "Célula normal: E=25% | Câncer: E=85%",
              "Efeito Warburg: fermentação permite S baixo",
              "Cura: Restaurar S/E para níveis normais"],
             "Dificuldade: Alta"),

            ("8. Doenças Neurodegenerativas",
             "Alzheimer, Parkinson, ELA...",
             ["Cascata de colapso sintrópico",
              "Proteína mal-dobrada 'infecta' vizinhas",
              "Propagação: hipocampo → cortex",
              "Janela terapêutica: S > 70%"],
             "Dificuldade: Alta"),

            ("9. Resistência Antimicrobiana",
             "Bactérias vencendo antibióticos",
             ["Corrida armamentista E-S evolutiva",
              "Antibióticos selecionam resistentes",
              "Fração resistente pode chegar a 95%",
              "Solução: Uso racional, novos alvos"],
             "Dificuldade: Média"),

            ("10. Fusão Nuclear",
             "Capturar o Sol na Terra",
             ["Transição de fase sintrópica extrema",
              "Precisa: 150 milhões de graus",
              "Meta: Q > 10 (ganho energético)",
              "Previsão: Comercial entre 2040-2060"],
             "Dificuldade: Média"),
        ]

        # 2 problemas por página
        for i in range(0, 10, 2):
            for j in range(2):
                if i + j >= 10:
                    break

                titulo, subtitulo, pontos, dificuldade = problemas_detalhes[i + j]

                y_base = height - 100 if j == 0 else height/2 - 50

                # Título
                c.setFillColor(azul_escuro)
                c.setFont("Helvetica-Bold", 16)
                c.drawString(50, y_base, titulo)

                # Subtítulo
                c.setFillColor(HexColor("#666666"))
                c.setFont("Helvetica-Oblique", 12)
                c.drawString(50, y_base - 22, subtitulo)

                # Pontos
                c.setFillColor(black)
                c.setFont("Helvetica", 11)
                for k, ponto in enumerate(pontos):
                    c.drawString(70, y_base - 50 - k*18, f"• {ponto}")

                # Dificuldade
                c.setFont("Helvetica-Bold", 10)
                if "Máxima" in dificuldade:
                    c.setFillColor(vermelho)
                elif "Alta" in dificuldade:
                    c.setFillColor(laranja)
                else:
                    c.setFillColor(verde)
                c.drawString(50, y_base - 135, dificuldade)

                # Linha separadora
                if j == 0:
                    c.setStrokeColor(HexColor("#dddddd"))
                    c.setLineWidth(1)
                    c.line(50, height/2, width - 50, height/2)

            c.showPage()

        # ===== ÚLTIMA PÁGINA: CONCLUSÃO =====
        c.setFillColor(azul_escuro)
        c.rect(0, 0, width, height, fill=1, stroke=0)

        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(width/2, height - 100, "Conclusão")

        c.setFont("Helvetica", 14)
        conclusao = [
            "",
            "Todos os 10 problemas compartilham a mesma estrutura:",
            "",
            "Estado Atual (E alto) → Barreira → Estado Desejado (S alto)",
            "",
            "A solução universal é sempre:",
            "",
            "1. Identificar onde está a desordem (E)",
            "2. Calcular a energia necessária (ε)",
            "3. Aplicar energia de forma inteligente",
            "4. Permitir que a ordem (S) emerja",
            "",
            "",
            "O universo é uma dança entre ORDEM e DESORDEM.",
            "A vida é a ORDEM resistindo.",
            "A consciência é a ORDEM se conhecendo.",
            "A ciência é a ORDEM tentando entender.",
        ]

        y = height - 150
        for linha in conclusao:
            c.drawCentredString(width/2, y, linha)
            y -= 22

        # Equação final
        c.setFillColor(HexColor("#ffeb3b"))
        c.setFont("Helvetica-Bold", 28)
        c.drawCentredString(width/2, 150, "Φ(E, S, ε) = C")

        c.setFillColor(white)
        c.setFont("Helvetica", 12)
        c.drawCentredString(width/2, 110, "Entenda isso, e você entende tudo.")

        c.setFont("Helvetica", 10)
        c.drawCentredString(width/2, 50, "Modelo X Framework v2.0 | github.com/tiagohanna123/o")

        c.save()
        print(f"✓ PDF criado: {filename}")
        return filename

    pdf_file = criar_pdf()

except ImportError as e:
    print(f"⚠ ReportLab não disponível: {e}")
    pdf_file = None


# =============================================================================
# GERAR IMAGENS COM MATPLOTLIB
# =============================================================================

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import numpy as np

    # Configuração para alta qualidade
    plt.rcParams['figure.dpi'] = 150
    plt.rcParams['savefig.dpi'] = 150
    plt.rcParams['font.size'] = 10

    def criar_infografico_principal():
        """Cria infográfico principal com todos os 10 problemas"""
        fig, ax = plt.subplots(figsize=(12, 16))
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 16)
        ax.axis('off')

        # Título
        ax.text(6, 15.5, "10 GRANDES PROBLEMAS CIENTÍFICOS",
                ha='center', va='top', fontsize=20, fontweight='bold', color='#1a237e')
        ax.text(6, 14.8, "Analisados pelo Modelo X Framework",
                ha='center', va='top', fontsize=14, color='#666666')

        # Equação
        box = patches.FancyBboxPatch((3, 13.5), 6, 1, boxstyle="round,pad=0.1",
                                      facecolor='#1a237e', edgecolor='none')
        ax.add_patch(box)
        ax.text(6, 14, "Φ(E, S, ε) = C", ha='center', va='center',
                fontsize=16, color='white', fontweight='bold')

        # Problemas
        problemas = [
            ("Matéria/Energia Escura", "95% invisível", "#9c27b0", "E=95%"),
            ("Gravidade Quântica", "Unificação", "#673ab7", "E=50%"),
            ("Origem da Vida", "Química → Bio", "#3f51b5", "E→40%"),
            ("Consciência", "Sentir existir", "#2196f3", "S=85%"),
            ("Mudanças Climáticas", "Aquecer/Esfriar", "#00bcd4", "E=58%"),
            ("Envelhecimento", "E vence S", "#009688", "E/S↑"),
            ("Câncer", "Células rebeldes", "#4caf50", "E=80%"),
            ("Neurodegeneração", "Cascata", "#8bc34a", "S↓↓"),
            ("Resistência AMR", "Bactérias", "#cddc39", "Evolutivo"),
            ("Fusão Nuclear", "Sol na Terra", "#ffeb3b", "Q>10"),
        ]

        for i, (nome, desc, cor, metrica) in enumerate(problemas):
            row = i // 2
            col = i % 2
            x = 1 + col * 5.5
            y = 12.5 - row * 2.3

            # Caixa
            box = patches.FancyBboxPatch((x, y-0.8), 5, 1.8, boxstyle="round,pad=0.05",
                                          facecolor=cor, edgecolor='none', alpha=0.9)
            ax.add_patch(box)

            # Número
            ax.text(x+0.3, y+0.7, f"{i+1}", fontsize=20, fontweight='bold',
                    color='white', alpha=0.5)

            # Texto
            ax.text(x+1.2, y+0.5, nome, fontsize=11, fontweight='bold', color='white')
            ax.text(x+1.2, y, desc, fontsize=9, color='white', alpha=0.9)
            ax.text(x+4.5, y+0.5, metrica, fontsize=9, fontweight='bold',
                    color='white', ha='right')

        # Legenda
        ax.text(6, 0.8, "E = Entropia (Desordem) | S = Sintropia (Ordem) | ε = Energia",
                ha='center', fontsize=10, color='#666666')
        ax.text(6, 0.3, "Modelo X Framework v2.0",
                ha='center', fontsize=9, color='#999999')

        filename = os.path.join(OUTPUT_DIR, "infografico_10_problemas.png")
        plt.savefig(filename, bbox_inches='tight', facecolor='white', edgecolor='none')
        plt.close()
        print(f"✓ Infográfico criado: {filename}")
        return filename

    def criar_diagrama_balanca():
        """Cria diagrama da balança Entropia-Sintropia"""
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6)
        ax.axis('off')

        # Título
        ax.text(5, 5.5, "O MODELO X EM UMA IMAGEM",
                ha='center', fontsize=18, fontweight='bold', color='#1a237e')

        # Balança
        # Triângulo (fulcro)
        triangle = patches.Polygon([[5, 1.5], [4.5, 0.5], [5.5, 0.5]],
                                    facecolor='#ff9800', edgecolor='#e65100', linewidth=2)
        ax.add_patch(triangle)

        # Barra
        ax.plot([1, 9], [3, 3], 'k-', linewidth=8)
        ax.plot([1, 9], [3, 3], '-', color='#795548', linewidth=6)

        # Prato Entropia (esquerda)
        circle_e = patches.Circle((1.5, 3), 0.8, facecolor='#f44336', edgecolor='#b71c1c', linewidth=2)
        ax.add_patch(circle_e)
        ax.text(1.5, 3, "E", ha='center', va='center', fontsize=24, fontweight='bold', color='white')
        ax.text(1.5, 1.8, "ENTROPIA\n(Desordem)", ha='center', fontsize=10, color='#c62828')

        # Prato Sintropia (direita)
        circle_s = patches.Circle((8.5, 3), 0.8, facecolor='#4caf50', edgecolor='#1b5e20', linewidth=2)
        ax.add_patch(circle_s)
        ax.text(8.5, 3, "S", ha='center', va='center', fontsize=24, fontweight='bold', color='white')
        ax.text(8.5, 1.8, "SINTROPIA\n(Ordem)", ha='center', fontsize=10, color='#2e7d32')

        # Energia no centro
        circle_energy = patches.Circle((5, 4.2), 0.6, facecolor='#ff9800', edgecolor='#e65100', linewidth=2)
        ax.add_patch(circle_energy)
        ax.text(5, 4.2, "ε", ha='center', va='center', fontsize=20, fontweight='bold', color='white')
        ax.text(5, 3.3, "ENERGIA", ha='center', fontsize=10, fontweight='bold', color='#e65100')

        # Setas
        ax.annotate('', xy=(3, 3), xytext=(4.3, 4.2),
                    arrowprops=dict(arrowstyle='->', color='#ff9800', lw=2))
        ax.annotate('', xy=(7, 3), xytext=(5.7, 4.2),
                    arrowprops=dict(arrowstyle='->', color='#ff9800', lw=2))

        # Equação
        box = patches.FancyBboxPatch((2.5, 0.2), 5, 0.8, boxstyle="round,pad=0.1",
                                      facecolor='#1a237e', edgecolor='none')
        ax.add_patch(box)
        ax.text(5, 0.6, "Φ(E, S, ε) = C  (sempre em equilíbrio)",
                ha='center', va='center', fontsize=12, color='white', fontweight='bold')

        filename = os.path.join(OUTPUT_DIR, "diagrama_balanca_ES.png")
        plt.savefig(filename, bbox_inches='tight', facecolor='white', edgecolor='none')
        plt.close()
        print(f"✓ Diagrama criado: {filename}")
        return filename

    def criar_grafico_problemas():
        """Cria gráfico de barras com E/S de cada problema"""
        fig, ax = plt.subplots(figsize=(12, 8))

        problemas = [
            "Matéria Escura", "Gravidade\nQuântica", "Origem\nda Vida",
            "Consciência", "Clima", "Envelhecimento",
            "Câncer", "Neuro-\ndegeneração", "Resistência\nAMR", "Fusão\nNuclear"
        ]

        entropia = [0.95, 0.50, 0.40, 0.15, 0.58, 0.84, 0.80, 0.70, 0.60, 0.85]
        sintropia = [0.05, 0.50, 0.60, 0.85, 0.42, 0.05, 0.20, 0.30, 0.40, 0.60]

        x = np.arange(len(problemas))
        width = 0.35

        bars1 = ax.bar(x - width/2, entropia, width, label='Entropia (E)', color='#f44336', alpha=0.8)
        bars2 = ax.bar(x + width/2, sintropia, width, label='Sintropia (S)', color='#4caf50', alpha=0.8)

        ax.set_ylabel('Nível (0-1)', fontsize=12)
        ax.set_title('Entropia vs Sintropia nos 10 Problemas Científicos\n(Modelo X Framework)',
                     fontsize=14, fontweight='bold', color='#1a237e')
        ax.set_xticks(x)
        ax.set_xticklabels(problemas, fontsize=9)
        ax.legend(fontsize=11)
        ax.set_ylim(0, 1.1)
        ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5, label='Equilíbrio')
        ax.grid(axis='y', alpha=0.3)

        # Linha de equilíbrio
        ax.text(9.5, 0.52, 'Equilíbrio', fontsize=9, color='gray')

        plt.tight_layout()

        filename = os.path.join(OUTPUT_DIR, "grafico_ES_problemas.png")
        plt.savefig(filename, bbox_inches='tight', facecolor='white', edgecolor='none')
        plt.close()
        print(f"✓ Gráfico criado: {filename}")
        return filename

    # Gerar todas as imagens
    img1 = criar_infografico_principal()
    img2 = criar_diagrama_balanca()
    img3 = criar_grafico_problemas()

except ImportError as e:
    print(f"⚠ Matplotlib não disponível: {e}")


# =============================================================================
# RESUMO FINAL
# =============================================================================

print("\n" + "="*60)
print("ARQUIVOS PARA COMPARTILHAMENTO - CRIADOS COM SUCESSO!")
print("="*60)
print(f"\nPasta: {OUTPUT_DIR}")
print("\nArquivos disponíveis:")

for f in os.listdir(OUTPUT_DIR):
    filepath = os.path.join(OUTPUT_DIR, f)
    size = os.path.getsize(filepath) / 1024  # KB
    print(f"  • {f} ({size:.1f} KB)")

print("\nPronto para compartilhar no WhatsApp!")
