import discord
from discord import app_commands
from discord.ext import commands
import os
import re
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURAÇÕES DO BOT (Substitua pelos seus IDs) ---
CONFIG = {
    "CANAL_DIVULGACAO_LIVE": 1502777768058814510,  # Substitua pelo ID do canal de lives (Número)
    "CANAL_DIVULGACAO_VIDEO": 1502777768058814509, # Substitua pelo ID do canal de vídeos (Número)
    "CARGO_LIVE_ON": 1502777759863144525,          # Substitua pelo ID do cargo Live On (Número)

    "MSG_PADRAO_LIVE": "**Vem pra live na cidade JardimPeri®**\n  **Segue, Curte, Comente e Compartilhe**",
    
    "MSG_PADRAO_VIDEO": "**Vem conferir o novo vídeo na cidade JardimPeri®**\n  **Segue, Curte, Comente e Compartilhe**"
}

# Banco de dados temporário para rastrear as lives ativas {user_id: message_id}
lives_ativas = {}

# RegExp para validar as plataformas permitidas
RE_PLATAFORMAS = re.compile(r'(tiktok\.com|instagram\.com|youtube\.com|youtu\.be|kick\.com|facebook\.com)', re.IGNORECASE)

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix="!", intents=intents)

TOKEN = os.getenv("TOKEN_JP")

    async def on_ready(self):
        print(f"🤖 Bot de divulgação online como {self.user}!")
        # Registra a View persistente para os botões continuarem funcionando se o bot reiniciar
        self.add_view(PainelDivulgacao())

bot = Bot()

# --- MODAIS ---

class ModalLive(discord.ui.Modal, title="🚀 Iniciar Nova Live"):
    link = discord.ui.TextInput(label="Link da Live", placeholder="https://tiktok.com/@username", style=discord.TextStyle.short, required=True)
    descricao = discord.ui.TextInput(label="Descrição (Opcional)", placeholder="Descreva sua live...", style=discord.TextStyle.long, required=False)

    async def on_submit(self, interaction: discord.Interaction):
        link_val = self.link.value
        desc_val = self.descricao.value if self.descricao.value else CONFIG["MSG_PADRAO_LIVE"]

        if not RE_PLATAFORMAS.search(link_val):
            embed_erro = discord.Embed(description="⚠️ Link inválido! Use apenas links de plataformas permitidas.", color=0xFF0000)
            return await interaction.response.send_message(embed=embed_erro, ephemeral=True)

        canal_divulgacao = interaction.guild.get_channel(CONFIG["CANAL_DIVULGACAO_LIVE"])
        cargo_live = interaction.guild.get_role(CONFIG["CARGO_LIVE_ON"])

        embed_live = discord.Embed(
            title="`🟢` `Online`",
            description=f"{desc_val}\n\n **Assista aqui:** \n**{link_val}**",
            color=0xFF0000
        )

        embed_live.set_thumbnail(url="https://cdn.discordapp.com/attachments/1444735189765849320/1503019230910746654/GIF_PERI.gif?ex=6a09bc3d&is=6a086abd&hm=4e07820a343bdd5a497b9f021dbc6b6d52aea9f9394b15ffb18eaf771be9f2d1&")

        embed_live.set_image(url="https://cdn.discordapp.com/attachments/1444735189765849320/1505098549610811462/Criadores_JP_2.png?ex=6a0a0c81&is=6a08bb01&hm=51d6cf0ae416af4e6f37516d9a39ab6bb4f6be70166faa799f9f36acdaa74e2b&")

        embed_live.set_footer(text="Jardim Peri RP - Todos os direitos reservados", icon_url="https://cdn.discordapp.com/attachments/1444735189765849320/1505074583601025114/emoji_JP.webp?ex=6a094d6f&is=6a07fbef&hm=5bd4e53ca8c4b641133b0f855affa243f440b86cdb33410d7579215042d8eba3&")

        # Envia o anúncio
        msg = await canal_divulgacao.send(content=f"@everyone  | {interaction.user.mention} está em live!", embed=embed_live)
        
        # Salva o ID da mensagem para fechar depois
        lives_ativas[interaction.user.id] = msg.id

        # Atribui o cargo
        if cargo_live:
            await interaction.user.add_roles(cargo_live)

        embed_sucesso = discord.Embed(description="✅ Live aberta com sucesso. <#1502777768058814510>", color=0xFF0000)
        await interaction.response.send_message(embed=embed_sucesso, ephemeral=True)


class ModalVideo(discord.ui.Modal, title="📹 Divulgar Novo Vídeo"):
    link = discord.ui.TextInput(label="Link do Vídeo", placeholder="https://tiktok.com/@username", style=discord.TextStyle.short, required=True)
    descricao = discord.ui.TextInput(label="Descrição (Opcional)", placeholder="Descreva seu vídeo...", style=discord.TextStyle.long, required=False)

    async def on_submit(self, interaction: discord.Interaction):
        link_val = self.link.value
        desc_val = self.descricao.value if self.descricao.value else CONFIG["MSG_PADRAO_VIDEO"]

        if not RE_PLATAFORMAS.search(link_val):
            embed_erro = discord.Embed(description="⚠️ Link inválido! Use apenas links de plataformas permitidas.", color=0xFF0000)
            return await interaction.response.send_message(embed=embed_erro, ephemeral=True)

        canal_divulgacao = interaction.guild.get_channel(CONFIG["CANAL_DIVULGACAO_VIDEO"])

        embed_video = discord.Embed(
            title="`🟢` `Vídeo Novo`",
            description=f"{desc_val}\n\n **Assista aqui:** **{link_val}**",
            color=0xFF0000
        )

        embed_video.set_thumbnail(url="https://cdn.discordapp.com/attachments/1444735189765849320/1503019230910746654/GIF_PERI.gif?ex=6a09bc3d&is=6a086abd&hm=4e07820a343bdd5a497b9f021dbc6b6d52aea9f9394b15ffb18eaf771be9f2d1&")

        embed_video.set_image(url="https://cdn.discordapp.com/attachments/1444735189765849320/1505098549610811462/Criadores_JP_2.png?ex=6a0a0c81&is=6a08bb01&hm=51d6cf0ae416af4e6f37516d9a39ab6bb4f6be70166faa799f9f36acdaa74e2b&")

        embed_video.set_footer(text="Jardim Peri RP - Todos os direitos reservados", icon_url="https://cdn.discordapp.com/attachments/1444735189765849320/1505074583601025114/emoji_JP.webp?ex=6a094d6f&is=6a07fbef&hm=5bd4e53ca8c4b641133b0f855affa243f440b86cdb33410d7579215042d8eba3&")

        await canal_divulgacao.send(content=f"@everyone  | {interaction.user.mention} divulgou um novo vídeo!", embed=embed_video)

        embed_sucesso = discord.Embed(description="✅ Vídeo divulgado com sucesso. <#1502777768058814509>", color=0xFF0000)
        await interaction.response.send_message(embed=embed_sucesso, ephemeral=True)


# --- PAINEL DE BOTÕES ---

# ID do cargo de Criador que terá permissão para usar os botões
CARGO_CRIADOR_ID = 1502777759863144526

class PainelDivulgacao(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) # timeout=None faz os botões durarem para sempre

    # Função auxiliar para verificar o cargo de Criador
    async def verificar_permissao(self, interaction: discord.Interaction) -> bool:
        cargo_criador = interaction.guild.get_role(CARGO_CRIADOR_ID)
        
        if not cargo_criador or cargo_criador not in interaction.user.roles:
            embed_negado = discord.Embed(
                description="❌ Você não tem permissão para usar este painel. Apenas Criadores podem divulgar.",
                color=0xFF0000
            )
            await interaction.response.send_message(embed=embed_negado, ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Iniciar Live", style=discord.ButtonStyle.gray, emoji="<:PLAY:1505319924841582693>", custom_id="btn_iniciar_live")
    async def iniciar_live(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await self.verificar_permissao(interaction):
            return
        await interaction.response.send_modal(ModalLive())

    @discord.ui.button(label="Fechar Live", style=discord.ButtonStyle.gray, emoji="<:STOP:1505319924841582693>", custom_id="btn_fechar_live")
    async def fechar_live(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await self.verificar_permissao(interaction):
            return

        msg_id = lives_ativas.get(interaction.user.id)

        if not msg_id:
            embed_erro = discord.Embed(description="❌ Você não possui nenhuma live ativa no momento.", color=0xFF0000)
            return await interaction.response.send_message(embed=embed_erro, ephemeral=True)

        cargo_live = interaction.guild.get_role(CONFIG["CARGO_LIVE_ON"])
        canal_divulgacao = interaction.guild.get_channel(CONFIG["CANAL_DIVULGACAO_LIVE"])

        try:
            # Remove o cargo
            if cargo_live and cargo_live in interaction.user.roles:
                await interaction.user.remove_roles(cargo_live)

            # Atualiza o Embed para Offline
            msg_original = await canal_divulgacao.fetch_message(msg_id)
            embed_original = msg_original.embeds[0]
            
            # Mantém o título novo de Offline, a descrição antiga e a cor vermelha
            embed_atualizado = discord.Embed(
                title="`🔴` `Offline`",
                description=embed_original.description,
                color=0xFF0000
            )
            
            # Mantém o autor se ele existir
            if embed_original.author:
                embed_atualizado.set_author(name=embed_original.author.name, icon_url=embed_original.author.icon_url)

            # FORÇA A MANUTENÇÃO DA THUMBNAIL, IMAGE E FOOTER DESEJADOS
            embed_atualizado.set_thumbnail(url="https://cdn.discordapp.com/attachments/1444735189765849320/1503019230910746654/GIF_PERI.gif?ex=6a09bc3d&is=6a086abd&hm=4e07820a343bdd5a497b9f021dbc6b6d52aea9f9394b15ffb18eaf771be9f2d1&")
            embed_atualizado.set_image(url="https://cdn.discordapp.com/attachments/1444735189765849320/1505098549610811462/Criadores_JP_2.png?ex=6a0a0c81&is=6a08bb01&hm=51d6cf0ae416af4e6f37516d9a39ab6bb4f6be70166faa799f9f36acdaa74e2b&")
            embed_atualizado.set_footer(text="Jardim Peri RP - Todos os direitos reservados", icon_url="https://cdn.discordapp.com/attachments/1444735189765849320/1505074583601025114/emoji_JP.webp?ex=6a094d6f&is=6a07fbef&hm=5bd4e53ca8c4b641133b0f855affa243f440b86cdb33410d7579215042d8eba3&")

            # Aplica a alteração na mensagem do Discord
            await msg_original.edit(embed=embed_atualizado)
            
            # Remove do banco temporário
            del lives_ativas[interaction.user.id]

            embed_sucesso = discord.Embed(description="❌ Live Fechada com sucesso.", color=0xFF0000)
            await interaction.response.send_message(embed=embed_sucesso, ephemeral=True)

        except Exception as e:
            print(e)
            await interaction.response.send_message("Ocorreu um erro ao tentar fechar a live.", ephemeral=True)

    @discord.ui.button(label="Divulgar Vídeo", style=discord.ButtonStyle.gray, emoji="<:PLAY:1505319924841582693>", custom_id="btn_divulgar_video")
    async def divulgar_video(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await self.verificar_permissao(interaction):
            return
        await interaction.response.send_modal(ModalVideo())


# --- COMANDO PARA ENVIAR O PAINEL ---

@bot.command(name="JP2")
@commands.has_permissions(administrator=True)
async def enviar_painel(ctx):
    embed = discord.Embed(
        title="<:PLAY:1505319924841582693> Painel de Divulgação",
        description="> Seja bem-vindo ao painel de Divulgação! Para fazer sua divulgação de conteúdo.\n\n"
        "> clique no botão abaixo e preencha o formulário com as informações solicitadas.\n\n"
        "> Obrigado por escolher o Jardim Peri!\n\n"
        "**Tenha em mãos as seguintes informações para agilizar sua divulgação:**\n\n"
        "🔸`Link do Conteúdo`\n"
        "🔸`Descrição do Conteúdo (Opcional)`",
        color=0xFF0000
    )

    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1444735189765849320/1503019230910746654/GIF_PERI.gif?ex=6a09bc3d&is=6a086abd&hm=4e07820a343bdd5a497b9f021dbc6b6d52aea9f9394b15ffb18eaf771be9f2d1&")

    embed.set_image(url="https://cdn.discordapp.com/attachments/1444735189765849320/1505098549610811462/Criadores_JP_2.png?ex=6a0a0c81&is=6a08bb01&hm=51d6cf0ae416af4e6f37516d9a39ab6bb4f6be70166faa799f9f36acdaa74e2b&")

    embed.set_footer(text="Jardim Peri RP - Todos os direitos reservados", icon_url="https://cdn.discordapp.com/attachments/1444735189765849320/1505074583601025114/emoji_JP.webp?ex=6a094d6f&is=6a07fbef&hm=5bd4e53ca8c4b641133b0f855affa243f440b86cdb33410d7579215042d8eba3&")

    await ctx.send(embed=embed, view=PainelDivulgacao())
    await ctx.message.delete()


bot.run(TOKEN)