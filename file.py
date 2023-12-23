import os
import pyshorteners
import qrcode
import streamlit as st


# Fonction pour raccourcir l'URL
def shorten_url(original_url):
    s = pyshorteners.Shortener()
    return s.tinyurl.short(original_url)


# Fonction pour générer le code QR
def generate_qr_code(shortened_url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(shortened_url)
    qr.make(fit=True)

    # Utiliser une partie du lien raccourci dans le nom du fichier
    filename = f"{shortened_url.split('/')[-1]}.png"
    img = qr.make_image(fill_color="red", back_color="white")
    img.save(filename)
    return filename


# Fonction pour générer les liens de partage pour différentes plateformes
def generate_social_share_links(original_url):
    twitter_url = f"https://twitter.com/intent/tweet?url={original_url}&text=Check%20this%20out&hashtags=ShareThis"
    facebook_url = f"https://www.facebook.com/sharer/sharer.php?u={original_url}"
    linkedin_url = f"https://www.linkedin.com/shareArticle?url={original_url}&title=Shared%20Link&summary=&source="

    return twitter_url, facebook_url, linkedin_url


def main():
    st.title("Raccourcisseur d'URL")

    # Formulaire pour saisir l'URL
    original_url = st.text_input("Saisissez votre URL à raccourcir:", "")

    if st.button("Raccourcir"):
        if original_url:
            # Raccourcir l'URL
            shortened_url = shorten_url(original_url)
            st.success(f"URL raccourcie: {shortened_url}")

            # Générer le code QR
            qr_filename = generate_qr_code(shortened_url)

            # Afficher l'image QR code
            st.image(image=qr_filename, caption="Code QR")

            # Partager sur les réseaux sociaux
            st.subheader("Partager sur les réseaux sociaux:")
            twitter_url, facebook_url, linkedin_url = generate_social_share_links(shortened_url)
            st.write(f"Partager sur Twitter: [Twitter]({twitter_url})")
            st.write(f"Partager sur Facebook: [Facebook]({facebook_url})")
            st.write(f"Partager sur LinkedIn: [LinkedIn]({linkedin_url}")

            # Effacer le fichier QR après l'affichage
            os.remove(qr_filename)
        else:
            st.warning("Veuillez saisir une URL valide.")


if __name__ == "__main__":
    main()
