
# import streamlit as st
# import os
# from PIL import Image
# from reportlab.lib.pagesizes import A4
# from reportlab.platypus import SimpleDocTemplate, Image as RLImage, Spacer
# import traceback # Import traceback for detailed error logging

# # --- Mock or Import Backend ---
# # It's crucial that these backend functions exist and work as expected.
# # For debugging, you might want to temporarily mock them.
# try:
#     from BACKEND import generate_panels, generate_image, process_comic
# except ImportError:
#     st.error("Failed to import BACKEND modules. Make sure BACKEND.py and its functions (generate_panels, generate_image, process_comic) exist.")
#     # Mock functions for testing UI if backend is missing/broken
#     def mock_generate_panels(prompt, style):
#         print("WARNING: Using MOCK generate_panels")
#         return [{"Description": f"Desc {i+1}", "Text": f"Panel {i+1} Text"} for i in range(6)]
#     def mock_generate_images(panel_data, style):
#         print("WARNING: Using MOCK generate_images")
#         # Create dummy files for testing if they don't exist
#         mock_paths = []
#         for i in range(6):
#             path = os.path.join(PANEL_FOLDER, f"mock_panel_{i+1}.png")
#             if not os.path.exists(path):
#                  try:
#                     # Create a small blank image
#                     img = Image.new('RGB', (60, 30), color = 'red')
#                     img.save(path)
#                     print(f"Created mock image: {path}")
#                  except Exception as e:
#                     print(f"Error creating mock image {path}: {e}")
#                     # Return fewer paths to simulate an error
#                     return mock_paths
#             mock_paths.append(path)
#         # Simulate returning fewer images sometimes for testing the error path
#         # import random
#         # if random.random() > 0.7:
#         #     print("Simulating returning fewer images")
#         #     return mock_paths[:4]
#         return mock_paths
#     def mock_process_comic(image_paths, panel_texts, output_path):
#         print(f"WARNING: Using MOCK process_comic. Output path: {output_path}")
#         # Create a dummy output file
#         try:
#             img = Image.new('RGB', (100, 150), color = 'blue')
#             img.save(output_path)
#             print(f"Created mock output comic: {output_path}")
#         except Exception as e:
#             print(f"Error creating mock output comic {output_path}: {e}")


#     # Uncomment below to use mocks if BACKEND is unavailable/broken
#     # generate_panels = generate_panels # Keep if real backend exists
#     # generate_image = generate_image   # Keep if real backend exists
#     # process_comic = process_comic     # Keep if real backend exists

#     # Or assign mocks if backend is the issue:
#     # generate_panels.generate_panels = mock_generate_panels
#     # generate_image.generate_images = mock_generate_images
#     # process_comic.create_comic_strip_with_text = mock_process_comic

# # --- Constants and Setup ---
# PANEL_FOLDER = "PANEL_IMAGES"
# OUTPUT_FOLDER = "OUTPUT"

# os.makedirs(PANEL_FOLDER, exist_ok=True)
# os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# STYLE_DESCRIPTIONS = {
#     "Manga": "High-contrast black and white sketch with sharp, clean lines, exaggerated facial expressions, and dramatic shading. No bright colors, only grayscale tones",
#     "Anime": "Vibrant colors with smooth cel shading, large expressive eyes, and detailed hair. Dynamic action poses with fluid motion lines",
#     "American": "Bold outlines with heavy inking, bright and saturated colors, and exaggerated muscular features. Classic comic book style",
#     "Belgian": "Clean, clear lines with soft, flat shading. Rich and detailed backgrounds in a semi-realistic style, inspired by Tintin comics",
# }

# # --- Streamlit UI ---
# st.title("🎨 ComicCrafter AI")
# st.write("Generate a 3x2 comic strip from your story prompt")

# # User inputs
# user_prompt = st.text_area("📝 Enter your story prompt", "")
# art_style = st.selectbox("🎨 Choose an art style", list(STYLE_DESCRIPTIONS.keys()))
# st.info(f"**Style Description:** {STYLE_DESCRIPTIONS[art_style]}")

# if st.button("🚀 Generate Comic"): # Changed button label slightly
#     if not user_prompt:
#         st.warning("⚠️ Please enter a story prompt.") # Changed to warning
#         st.stop() # Stop execution if no prompt

#     panel_data = None
#     image_paths = []
#     panel_texts = []

#     try:
#         with st.spinner("⏳ Generating panel descriptions & dialogues..."):
#             # Ensure generate_panels is correctly imported and called
#             panel_data = generate_panels.generate_panels(user_prompt, art_style)
#             st.write("Debug: Panel Data Generated:") # DEBUG
#             st.json(panel_data) # DEBUG - Use st.json for better display of lists/dicts

#             # --- Validation for panel_data ---
#             if not isinstance(panel_data, list) or len(panel_data) != 6:
#                 st.error(f"❌ Error: Expected 6 panel descriptions, but received {len(panel_data) if isinstance(panel_data, list) else 'invalid data'}. Backend 'generate_panels' might have failed.")
#                 st.write("Received Data:", panel_data) # Show what was received
#                 st.stop()
#             # Check if structure is as expected (assuming 'Text' and 'Description' keys)
#             if not all(isinstance(p, dict) and "Text" in p and "Description" in p for p in panel_data):
#                  st.error(f"❌ Error: Panel data structure is incorrect. Expected list of dicts with 'Text' and 'Description'.")
#                  st.stop()

#             panel_texts = [panel["Text"] for panel in panel_data] # Extract texts only after validation

#         with st.spinner("⏳ Generating images for comic panels..."):
#             # Ensure generate_images is correctly imported and called
#             # generate_images *should* return a list of file paths
#             # If it returns a generator, convert it to a list immediately
#             image_paths_iterable = generate_image.generate_images(panel_data, art_style)
#             image_paths = list(image_paths_iterable) # Convert to list

#             st.write(f"Debug: Received {len(image_paths)} image paths from generate_images.") # DEBUG
#             st.write("Debug: Image Paths List:") # DEBUG
#             st.write(image_paths) # DEBUG

#         # --- Detailed Check for Image Paths ---
#         st.write("--- Debugging Image Path Check ---") # DEBUG
#         paths_ok = True
#         if len(image_paths) != 6:
#             st.warning(f"⚠️ Expected 6 image paths, but received {len(image_paths)}.")
#             paths_ok = False
#         else:
#             for i, img_path in enumerate(image_paths):
#                 is_str = isinstance(img_path, str)
#                 exists = os.path.exists(img_path) if is_str else False
#                 st.write(f"Path {i+1}: '{img_path}' | Type: {type(img_path)} | Is String: {is_str} | Exists: {exists}") # DEBUG
#                 if not is_str or not exists:
#                     paths_ok = False
#                     st.warning(f"   -> Problem detected with path {i+1}!") # DEBUG Highlight issue
#         st.write("--- End Debugging ---") # DEBUG

#         # --- Main Logic ---
#         if paths_ok:
#             # Ensure process_comic is correctly imported and called
#             output_image_path = os.path.join(OUTPUT_FOLDER, "comic_strip_with_text.png")

#             with st.spinner("🎨 Assembling comic strip..."):
#                 process_comic.create_comic_strip_with_text(image_paths, panel_texts, output_image_path)

#             if os.path.exists(output_image_path):
#                 st.image(output_image_path, caption="✅ Your Comic Strip", use_container_width=True)
#                 st.success(" Comic generated successfully!")

#                 # --- PDF Generation ---
#                 pdf_output_path = os.path.join(OUTPUT_FOLDER, "comic_strip.pdf")

#                 # Define PDF creation function *inside* the successful block or globally
#                 def create_pdf(image_path, pdf_output_path):
#                     """Generate a PDF from the final comic strip"""
#                     try:
#                         doc = SimpleDocTemplate(pdf_output_path, pagesize=A4)
#                         # Calculate aspect ratio to fit A4 better if needed
#                         img_width, img_height = Image.open(image_path).size
#                         aspect = img_height / float(img_width)
#                         page_width, page_height = A4 # A4 dimensions
#                         # Try to fit width, adjust height proportionally
#                         display_width = page_width * 0.8 # Use 80% of page width
#                         display_height = display_width * aspect

#                         # If height exceeds page height, scale down further
#                         max_height = page_height * 0.8
#                         if display_height > max_height:
#                             display_height = max_height
#                             display_width = display_height / aspect

#                         rl_img = RLImage(image_path, width=display_width, height=display_height)
#                         spacer = Spacer(1, 20) # Add some space below the image

#                         story = [rl_img, spacer]
#                         doc.build(story)
#                         return True
#                     except Exception as e:
#                         st.error(f"❌ Failed to create PDF: {e}")
#                         print(traceback.format_exc()) # Print detailed error to console
#                         return False

#                 if create_pdf(output_image_path, pdf_output_path):
#                     # PDF Download Button
#                     try:
#                         with open(pdf_output_path, "rb") as pdf_file:
#                             st.download_button(
#                                 label="⬇️ Download Comic as PDF",
#                                 data=pdf_file,
#                                 file_name="comic_strip.pdf",
#                                 mime="application/pdf"
#                             )
#                     except FileNotFoundError:
#                         st.error("❌ PDF file not found for download.")
#                     except Exception as e:
#                         st.error(f"❌ Error providing PDF download: {e}")

#             else:
#                 st.error("❌ Error: Final comic image file was not created by 'process_comic'.")

#         else:
#             # This else corresponds to `if paths_ok:`
#             st.error("❌ Something went wrong! Image generation failed or produced invalid/missing files. Check the debug messages above.")
#             st.info("Possible reasons: Issues with the image generation backend, file saving permissions, or incorrect paths returned.")

#     except Exception as e:
#         st.error(f"💥 An unexpected error occurred during comic generation!")
#         st.error(f"Error details: {e}")
#         # Print traceback to the console where streamlit is running for more detail
#         print("--- Full Traceback ---")
#         print(traceback.format_exc())
#         print("--- End Traceback ---")
#         st.warning("Please check the console output for more technical details.")

# # Optional: Add a section to clear generated files if needed
# # if st.button("Clear Generated Files"):
# #     # Be careful with file deletion!
# #     # ... add code to remove files in PANEL_FOLDER and OUTPUT_FOLDER ...
# #     st.success("Generated files cleared.")






import streamlit as st
import os
import base64 # Needed for background image
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Image as RLImage, Spacer
import traceback

# --- Backend Import ---
# Assuming BACKEND.py with generate_panels, generate_image, process_comic exists
try:
    from BACKEND import generate_panels, generate_image, process_comic
    BACKEND_AVAILABLE = True
except ImportError:
    st.error("🚨 Failed to import BACKEND modules. Ensure BACKEND.py exists with required functions.")
    BACKEND_AVAILABLE = False
    # Define dummy functions if backend is missing, so the UI can still load partially
    def generate_panels(prompt, style): return [{"Description": f"Mock Desc {i+1}", "Text": f"Mock Panel {i+1}"} for i in range(6)]
    def generate_image(panel_data, style): return [] # Return empty list to show error path
    def process_comic(image_paths, panel_texts, output_path): pass

# --- Constants and Setup ---
PANEL_FOLDER = "PANEL_IMAGES"
OUTPUT_FOLDER = "OUTPUT"
BACKGROUND_IMAGE_FILE = "background.png" # Name of your background image file

os.makedirs(PANEL_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

STYLE_DESCRIPTIONS = {
    "Manga": "🇯🇵 High-contrast B&W sketch, sharp lines, exaggerated expressions, dramatic shading.",
    "Anime": "🌸 Vibrant colors, cel shading, large expressive eyes, detailed hair, dynamic poses.",
    "American": "💥 Bold outlines, heavy inking, bright saturated colors, exaggerated muscular features.",
    "Belgian": " Tintin-style. Clean lines, soft flat shading, rich detailed backgrounds, semi-realistic.",
}

# --- Function to Add Background Image ---
# (Uses CSS injection - a common Streamlit technique)
@st.cache_data # Cache the function to avoid reloading image on every interaction
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    try:
        bin_str = get_base64_of_bin_file(png_file)
        page_bg_img = f'''
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed; # Keeps the background fixed while scrolling
        }}
        /* Optional: Add slight transparency to main block for better readability */
        [data-testid="stMain"] {{
            background-color: rgba(255, 255, 255, 0.85); /* White with 85% opacity */
            border-radius: 10px; /* Optional: rounded corners */
            padding: 20px; /* Optional: add padding */
        }}
        /* Optional: Style buttons */
        .stButton>button {{
            background-color: #FF4B4B; /* Streamlit red */
            color: white;
            border-radius: 5px;
            padding: 0.5em 1em;
            border: none;
            font-weight: bold;
        }}
        .stButton>button:hover {{
            background-color: #E03C3C;
            color: white;
        }}
        </style>
        '''
        st.markdown(page_bg_img, unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"⚠️ Background image '{png_file}' not found. Skipping background.", icon="🖼️")
    except Exception as e:
        st.error(f"An error occurred setting background: {e}")

# --- Apply Background ---
if os.path.exists(BACKGROUND_IMAGE_FILE):
    set_png_as_page_bg(BACKGROUND_IMAGE_FILE)
else:
    st.warning(f"⚠️ Background image file '{BACKGROUND_IMAGE_FILE}' not found in the script directory.", icon="🖼️")


# --- Streamlit UI ---
st.title("🎨 ComicCrafter AI ✨")
st.caption("Turn your stories into awesome 3x2 comic strips!")
st.divider()

# --- UI Enhancements: Columns for Layout ---
col1, col2 = st.columns([3, 1]) # Give more space to the text area

with col1:
    st.subheader("1. Enter Your Story Idea")
    user_prompt = st.text_area("📝 Story Prompt:", "", height=150, placeholder="e.g., A robot trying to learn how to bake a cake, causing chaos in the kitchen.")

with col2:
    st.subheader("2. Choose Style")
    # Use radio buttons or selectbox - selectbox is better for more styles
    art_style = st.selectbox("🎨 Art Style:", list(STYLE_DESCRIPTIONS.keys()))
    # Display description prominently
    st.markdown(f"**Style Preview:**")
    st.info(f"{STYLE_DESCRIPTIONS[art_style]}", icon="🖌️")


st.divider()

# --- Generation Button ---
st.subheader("3. Generate!")
generate_button = st.button("🚀 Generate Comic Strip", use_container_width=True)

# --- Processing Logic (when button is clicked) ---
if generate_button:
    if not user_prompt:
        st.warning("⚠️ Please enter a story prompt before generating.", icon="✍️")
        st.stop() # Stop execution if no prompt

    if not BACKEND_AVAILABLE:
         st.error("🚨 Backend functions are unavailable. Cannot generate comic.")
         st.stop()

    # Initialize variables for this run
    panel_data = None
    image_paths = []
    panel_texts = []
    success = False # Flag to track overall success

    try:
        # --- Step 1: Generate Panels ---
        with st.spinner("⏳ Step 1/3: Generating panel descriptions & dialogues..."):
            panel_data = generate_panels.generate_panels(user_prompt, art_style)
            # Add a small visible confirmation inside the spinner context if desired
            # st.write("Panel data structure received.")

        # --- Validation for panel_data ---
        # Moved validation after the first step
        if not isinstance(panel_data, list) or len(panel_data) != 6:
            st.error(f"❌ Error: Expected 6 panel descriptions, but received {len(panel_data) if isinstance(panel_data, list) else 'invalid data'} from `generate_panels`.")
            st.write("Received Data:", panel_data) # Show what was received
            st.stop()
        if not all(isinstance(p, dict) and "Text" in p and "Description" in p for p in panel_data):
             st.error(f"❌ Error: Panel data structure from `generate_panels` is incorrect. Expected list of dicts with 'Text' and 'Description'.")
             st.write("Received Data:", panel_data)
             st.stop()

        # Extract texts only after validation is passed
        panel_texts = [panel["Text"] for panel in panel_data]

        # --- Step 2: Generate Images ---
        with st.spinner("⏳ Step 2/3: Generating images for comic panels... (This may take a while!)"):
            # Ensure generate_images returns a list (convert if it's a generator)
            image_paths_iterable = generate_image.generate_images(panel_data, art_style)
            image_paths = list(image_paths_iterable)
            # st.write(f"Received {len(image_paths)} image paths.") # Optional debug

        # --- Validation for Image Paths ---
        paths_ok = False # Assume not okay initially
        if len(image_paths) == 6:
            # Check if all paths are strings and exist *after* generation attempt
            all_valid = True
            for i, img_path in enumerate(image_paths):
                is_str = isinstance(img_path, str)
                exists = os.path.exists(img_path) if is_str else False
                if not is_str or not exists:
                    all_valid = False
                    st.warning(f"⚠️ Problem with generated path/file for panel {i+1}: '{img_path}' (String: {is_str}, Exists: {exists})")
                    break # Stop checking on first error
            if all_valid:
                paths_ok = True
        else:
            st.warning(f"⚠️ Expected 6 image paths from `generate_images`, but received {len(image_paths)}.")


        # --- Step 3: Assemble Comic and Create PDF (if images are OK) ---
        if paths_ok:
            output_image_path = os.path.join(OUTPUT_FOLDER, "comic_strip_with_text.png")
            pdf_output_path = os.path.join(OUTPUT_FOLDER, "comic_strip.pdf")

            with st.spinner("⏳ Step 3/3: Assembling comic strip and PDF..."):
                # --- Assemble the comic strip image ---
                process_comic.create_comic_strip_with_text(image_paths, panel_texts, output_image_path)

                # --- Create PDF ---
                def create_pdf(image_path, pdf_output_path):
                    """Generate a PDF from the final comic strip"""
                    # Check if final image exists before trying to make PDF
                    if not os.path.exists(image_path):
                        st.error(f"❌ Cannot create PDF: Final comic image '{image_path}' not found.")
                        return False
                    try:
                        doc = SimpleDocTemplate(pdf_output_path, pagesize=A4, leftMargin=30, rightMargin=30, topMargin=30, bottomMargin=30)
                        # Calculate aspect ratio to fit A4 better
                        with Image.open(image_path) as img_pil:
                             img_width, img_height = img_pil.size

                        aspect = img_height / float(img_width)
                        page_width, page_height = A4 # A4 dimensions (points)
                        # Use ~90% of page width
                        display_width = page_width * 0.9
                        display_height = display_width * aspect

                        # If height exceeds usable page height, scale down further
                        max_height = page_height * 0.9
                        if display_height > max_height:
                            display_height = max_height
                            display_width = display_height / aspect

                        rl_img = RLImage(image_path, width=display_width, height=display_height)
                        # Center the image (optional)
                        rl_img.hAlign = 'CENTER'
                        spacer = Spacer(1, 20) # Add some space below the image

                        story = [rl_img, spacer]
                        doc.build(story)
                        return True
                    except Exception as pdf_err:
                        st.error(f"❌ Failed to create PDF: {pdf_err}")
                        print(traceback.format_exc()) # Print detailed error to console
                        return False

                pdf_created = create_pdf(output_image_path, pdf_output_path)

            # --- Display Results ---
            if os.path.exists(output_image_path):
                st.subheader("🎉 Your Comic Strip!")
                st.image(output_image_path, caption="Your Generated Comic Strip", use_container_width=True)
                st.success("✅ Comic generated successfully!")
                success = True # Mark overall success

                # --- PDF Download Button (only if PDF was created) ---
                if pdf_created and os.path.exists(pdf_output_path):
                    try:
                        with open(pdf_output_path, "rb") as pdf_file:
                            st.download_button(
                                label="⬇️ Download Comic as PDF",
                                data=pdf_file,
                                file_name="comic_strip.pdf",
                                mime="application/pdf",
                                use_container_width=True # Make button wider
                            )
                    except FileNotFoundError:
                        st.error("❌ PDF file not found for download, although creation was reported successful.")
                    except Exception as dl_err:
                        st.error(f"❌ Error providing PDF download: {dl_err}")
                elif pdf_created: # PDF reported created, but file doesn't exist
                     st.error(f"❌ PDF file '{pdf_output_path}' seems to be missing after creation attempt.")
                # else: PDF creation failed, error already shown

            else:
                 st.error("❌ Error: Final comic image file was not found after 'process_comic' step.")

        else:
            # This else corresponds to `if paths_ok:`
            st.error("❌ Something went wrong! Image generation failed or produced invalid/missing files.")
            st.info("Possible reasons: Issues with the image generation backend (check terminal logs for API errors like 403 Forbidden or rate limits), file saving permissions, or incorrect paths returned.")

    except Exception as e:
        st.error(f"💥 An unexpected error occurred during the comic generation process!")
        # Use st.expander for long error details to keep UI cleaner
        with st.expander("Show Error Details"):
            st.error(f"{e}")
            st.code(traceback.format_exc()) # Show traceback in the app
        print("--- Full Traceback ---") # Also print to console
        print(traceback.format_exc())
        print("--- End Traceback ---")
        st.warning("Please check the error details above or the console output.")

    # Optional: Add a final status message outside the try/except
    # if success:
    #    st.balloons() # Add some fun on success

# --- Optional Footer ---
st.divider()
st.caption("ComicCrafter AI - Using Clipdrop & ReportLab")