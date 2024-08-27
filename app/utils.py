import io
from PIL import Image
import PyPDF2
import logging

logger = logging.getLogger(__name__)

def extract_images_from_pdf(pdf_content: bytes) -> list[Image.Image]:
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
        images = []
        for page_num, page in enumerate(pdf_reader.pages, 1):
            if '/XObject' in page['/Resources']:
                xObject = page['/Resources']['/XObject'].get_object()
                for obj in xObject:
                    if xObject[obj]['/Subtype'] == '/Image':
                        try:
                            size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                            data = xObject[obj].get_data()
                            img = Image.frombytes('RGB', size, data)
                            images.append(img)
                        except Exception as e:
                            logger.warning(f"Error extracting image from page {page_num}: {str(e)}")
                            continue
        logger.info(f"Extracted {len(images)} images from the PDF")
        return images
    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")


