import streamlit as st


#Side bar details
# def render_sidebar():
st.sidebar.title("🌙 Navigation")
st.sidebar.subheader("Quick Links")
st.sidebar.markdown("- 🏠 Home\n- 🗺️ Explore\n- 📞 Contact")

# def run_app():
#     apply_dark_theme()
#     render_sidebar()

#     # Image on Main Page
#     st.image("/Users/neeraj/Downloads/dino-reichmuth-A5rCN8626Ck-unsplash.jpg", 
#              caption="Your next adventure awaits!", 
#              use_container_width=True)

#     st.title("🌍 Travel agent to help you travel easier, safer and more convenient")

#     # Phone number input
#     user_phone_number = st.text_input("Enter your phone number")

#     # Preferences
#     user_preferrence_1_options = ['Mountains', 'Beaches', 'Desert', 'Riverside']
#     user_preferrence_2_options = ['Relaxed', 'Packed', 'Balanced']
#     profile = None

#     if st.button("Check Profile"):
#         if profile:
#             name = profile.get("name", "User")
#             st.write(f"Welcome {name} to your profile!")
#         else:
#             st.info("It seems you don't have an account. Please provide your preferences to create one.")

#             auth_number = st.text_input("Re-enter your mobile number for verification:")
#             user_preferrence_1 = st.multiselect("What types of destinations do you like?", user_preferrence_1_options)
#             user_preferrence_2 = st.multiselect("What kind of travel do you prefer?", user_preferrence_2_options)
#             user_preferrence_3 = st.text_input("Tell us about places you've visited in the past")

#             if st.button("Submit Preferences"):
#                 st.success("Thanks! Your preferences have been saved.")

# # 🔁 Run the app
# if __name__ == "__main__":
#     run_app()
