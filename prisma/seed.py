from prisma import Prisma
import bcrypt
import json
import numpy as np
from datetime import datetime

from prisma import Prisma
import bcrypt
import json
import numpy as np
from datetime import datetime

# Replace Cohere with LangChain imports
from langchain_community.embeddings import HuggingFaceEmbeddings
from typing import List, Optional

# Initialize LangChain embedding model
# Using all-MiniLM-L6-v2 which outputs 384-dimensional embeddings
embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def generate_embedding(text: str) -> List[float]:
    """Generate embeddings using HuggingFace model via LangChain."""
    if not text:
        return [0] * 1024  # Return zeros vector of proper dimension
    
    # Get embeddings from the model
    embedding = embeddings_model.embed_query(text)
    
    # Pad or truncate to 1024 dimensions to match your DB schema
    if len(embedding) < 1024:
        padding = [0] * (1024 - len(embedding))
        embedding.extend(padding)
    elif len(embedding) > 1024:
        embedding = embedding[:1024]
        
    return embedding

def generate_form_embeddings(name: str, description: Optional[str] = None) -> List[float]:
    """Generate embeddings for a form based on its name and description."""
    text = name
    if description:
        text += " " + description
    
    return generate_embedding(text)

# Initialize Prisma client
prisma = Prisma()

async def main():
    # Connect to the database
    await prisma.connect()
    
    # Create roles
    admin_role = await prisma.role.create(
        data={
            "name": "Admin",
            "description": "Administrator role with full access"
        }
    )
    
    user_role = await prisma.role.create(
        data={
            "name": "User",
            "description": "Regular user with limited access"
        }
    )
    
    # Create users
    admin_password = bcrypt.hashpw("admin123".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    admin_user = await prisma.user.create(
        data={
            "email": "admin@example.com",
            "password": admin_password,
            "name": "Admin User",
            "additional_info": json.dumps({"department": "Legal", "position": "Administrator"}),
            "roleId": admin_role.id
        }
    )
    
    user_password = bcrypt.hashpw("user123".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    regular_user = await prisma.user.create(
        data={
            "email": "user@example.com",
            "password": user_password,
            "name": "Regular User",
            "additional_info": json.dumps({"department": "Finance", "position": "Analyst"}),
            "roleId": user_role.id
        }
    )
    
    # Create form fields for copyright notice form (Form XVI)
    owner_field = await prisma.formfield.create(
        data={
            "label": "Copyright Owner",
            "description": "Full name of the copyright owner",
            "fieldType": "TEXT",
            "isRequired": True,
            "validations": json.dumps({"minLength": 3, "maxLength": 100})
        }
    )
    
    work_description_field = await prisma.formfield.create(
        data={
            "label": "Work Description",
            "description": "Description of the work for which copyright is claimed",
            "fieldType": "TEXTAREA",
            "isRequired": True,
            "validations": json.dumps({"minLength": 10, "maxLength": 500})
        }
    )
    
    copies_count_field = await prisma.formfield.create(
        data={
            "label": "Number of Infringing Copies",
            "description": "Number of infringing copies expected to arrive",
            "fieldType": "NUMBER",
            "isRequired": True,
            "validations": json.dumps({"min": 1})
        }
    )
    
    arrival_time_field = await prisma.formfield.create(
        data={
            "label": "Expected Arrival Time",
            "description": "Expected time of arrival of infringing copies",
            "fieldType": "DATE",
            "isRequired": True,
            "validations": json.dumps({})
        }
    )
    
    arrival_place_field = await prisma.formfield.create(
        data={
            "label": "Arrival Place",
            "description": "Expected place of arrival of infringing copies",
            "fieldType": "TEXT",
            "isRequired": True,
            "validations": json.dumps({"minLength": 3, "maxLength": 100})
        }
    )
    
    detention_period_field = await prisma.formfield.create(
        data={
            "label": "Detention Period",
            "description": "Period for which goods should be treated as prohibited",
            "fieldType": "NUMBER",
            "isRequired": True,
            "validations": json.dumps({"min": 1, "max": 90})
        }
    )
    
    name_address_field = await prisma.formfield.create(
        data={
            "label": "Full Name and Address",
            "description": "Full name and address of the person giving notice",
            "fieldType": "TEXTAREA",
            "isRequired": True,
            "validations": json.dumps({"minLength": 10, "maxLength": 300})
        }
    )
    
    work_class_field = await prisma.formfield.create(
        data={
            "label": "Class of Work",
            "description": "Class of the work (Literary, Dramatic, Musical, etc.)",
            "fieldType": "SELECT",
            "isRequired": True,
            "validations": json.dumps({
                "options": ["Literary", "Dramatic", "Musical", "Artistic", "Cinematograph Film", "Sound Recording"]
            })
        }
    )
    
    work_title_field = await prisma.formfield.create(
        data={
            "label": "Title of Work",
            "description": "Title of the work",
            "fieldType": "TEXT",
            "isRequired": True,
            "validations": json.dumps({"minLength": 1, "maxLength": 200})
        }
    )
    
    author_details_field = await prisma.formfield.create(
        data={
            "label": "Author Details",
            "description": "Full name, address and nationality of the author",
            "fieldType": "TEXTAREA",
            "isRequired": True,
            "validations": json.dumps({"minLength": 10, "maxLength": 300})
        }
    )
    
    work_language_field = await prisma.formfield.create(
        data={
            "label": "Language of Work",
            "description": "Language in which the work is written",
            "fieldType": "TEXT",
            "isRequired": True,
            "validations": json.dumps({"minLength": 2, "maxLength": 50})
        }
    )
    
    publisher_field = await prisma.formfield.create(
        data={
            "label": "Publisher Details",
            "description": "Name and address of the publisher",
            "fieldType": "TEXTAREA",
            "isRequired": True,
            "validations": json.dumps({"minLength": 10, "maxLength": 300})
        }
    )
    
    first_pub_year_field = await prisma.formfield.create(
        data={
            "label": "Year of First Publication",
            "description": "Year when the work was first published",
            "fieldType": "NUMBER",
            "isRequired": True,
            "validations": json.dumps({"min": 1800, "max": 2025})
        }
    )
    
    first_pub_country_field = await prisma.formfield.create(
        data={
            "label": "Country of First Publication",
            "description": "Country where the work was first published",
            "fieldType": "TEXT",
            "isRequired": True,
            "validations": json.dumps({"minLength": 2, "maxLength": 100})
        }
    )
    
    registration_num_field = await prisma.formfield.create(
        data={
            "label": "Registration Number",
            "description": "If the copyright is registered under section 45, the registration number",
            "fieldType": "TEXT",
            "isRequired": False,
            "validations": json.dumps({"minLength": 0, "maxLength": 50})
        }
    )
    
    origin_country_field = await prisma.formfield.create(
        data={
            "label": "Country of Origin of Infringing Copies",
            "description": "Country where the infringing copies originated",
            "fieldType": "TEXT",
            "isRequired": True,
            "validations": json.dumps({"minLength": 2, "maxLength": 100})
        }
    )
    
    importer_details_field = await prisma.formfield.create(
        data={
            "label": "Importer Details",
            "description": "Name, address and nationality of the importer in India",
            "fieldType": "TEXTAREA",
            "isRequired": True,
            "validations": json.dumps({"minLength": 10, "maxLength": 300})
        }
    )
    
    maker_details_field = await prisma.formfield.create(
        data={
            "label": "Maker Details",
            "description": "Name, address and nationality of the maker of the infringing copies",
            "fieldType": "TEXTAREA",
            "isRequired": True,
            "validations": json.dumps({"minLength": 10, "maxLength": 300})
        }
    )
    
    identify_willingness_field = await prisma.formfield.create(
        data={
            "label": "Identification Willingness",
            "description": "Will you be prepared to identify the copies to the satisfaction of the Commissioner of Customs?",
            "fieldType": "CHECKBOX",
            "isRequired": True,
            "validations": json.dumps({})
        }
    )
    
    fee_payment_field = await prisma.formfield.create(
        data={
            "label": "Fee Payment Details",
            "description": "Particulars of payment (Postal Order/Bank Draft/Treasury Challan number)",
            "fieldType": "TEXT",
            "isRequired": True,
            "validations": json.dumps({"minLength": 5, "maxLength": 100})
        }
    )
    
    additional_info_field = await prisma.formfield.create(
        data={
            "label": "Additional Information",
            "description": "Any other relevant information not covered above",
            "fieldType": "TEXTAREA",
            "isRequired": False,
            "validations": json.dumps({"minLength": 0, "maxLength": 500})
        }
    )
    
    upload_work_copy_field = await prisma.formfield.create(
        data={
            "label": "Copy of Work",
            "description": "Upload a copy of the work for which copyright is claimed",
            "fieldType": "FILE",
            "isRequired": True,
            "validations": json.dumps({"fileTypes": ["pdf", "docx", "jpg", "png"], "maxSize": 10})
        }
    )
    
    upload_ownership_evidence_field = await prisma.formfield.create(
        data={
            "label": "Evidence of Ownership",
            "description": "Upload evidence of ownership and authorship of copyright in the work",
            "fieldType": "FILE",
            "isRequired": True,
            "validations": json.dumps({"fileTypes": ["pdf", "docx", "jpg", "png"], "maxSize": 10})
        }
    )
    
    upload_infringement_evidence_field = await prisma.formfield.create(
        data={
            "label": "Evidence of Infringement",
            "description": "Upload evidence of infringement of copyright",
            "fieldType": "FILE",
            "isRequired": True,
            "validations": json.dumps({"fileTypes": ["pdf", "docx", "jpg", "png"], "maxSize": 10})
        }
    )
    
    upload_import_evidence_field = await prisma.formfield.create(
        data={
            "label": "Evidence of Import",
            "description": "Upload evidence of infringing copies being brought to India",
            "fieldType": "FILE",
            "isRequired": True,
            "validations": json.dumps({"fileTypes": ["pdf", "docx", "jpg", "png"], "maxSize": 10})
        }
    )
    
    upload_fee_evidence_field = await prisma.formfield.create(
        data={
            "label": "Evidence of Fee Payment",
            "description": "Upload evidence of payment of fee (copy of Postal Order/Bank Draft/Treasury Challan)",
            "fieldType": "FILE",
            "isRequired": True,
            "validations": json.dumps({"fileTypes": ["pdf", "docx", "jpg", "png"], "maxSize": 5})
        }
    )
    
    # Create Form for Copyright Notice (Form XVI)
    # Generate a random embedding vector of dimension 1024
    
    form_description = """
    Form XVI NOTICE UNDER SECTION 53 OF THE ACT (See rule 79)
    For reporting copyright infringement to the Commissioner of Customs, Central Board of Excise and Customs,
    New Delhi, in accordance with section 53 of the Copyright Act, 1957 (14 of 1957).
    """
    form_title = "Form XVI NOTICE UNDER SECTION 53 OF THE ACT (See rule 79)"
    embedding_vector = [float(val) for val in generate_form_embeddings("Form XVI NOTICE UNDER SECTION 53 OF THE ACT (See rule 79)", description= form_description)]    
    form = await prisma.execute_raw(
            """
            INSERT INTO forms (title, description, embeddings, "createdAt", "updatedAt")
            VALUES ($1, $2, $3::vector(1024), NOW(), NOW())
            RETURNING id;
            """,
            form_title, form_description, embedding_vector
        )
    
    # Associate fields with the form
    field_order = 1
    for field in [
        owner_field, work_description_field, copies_count_field, arrival_time_field,
        arrival_place_field, detention_period_field, name_address_field, work_class_field,
        work_title_field, author_details_field, work_language_field, publisher_field,
        first_pub_year_field, first_pub_country_field, registration_num_field,
        origin_country_field, importer_details_field, maker_details_field, 
        identify_willingness_field, fee_payment_field, additional_info_field,
        upload_work_copy_field, upload_ownership_evidence_field, upload_infringement_evidence_field,
        upload_import_evidence_field, upload_fee_evidence_field
    ]:
        await prisma.formfieldonform.create(
            data={
                "formId": copyright_form.id,
                "fieldId": field.id,
                "order": field_order
            }
        )
        field_order += 1
    
    # Create a sample form submission (DRAFT status)
    form_submission = await prisma.formsubmission.create(
        data={
            "formId": copyright_form.id,
            "userId": regular_user.id,
            "status": "DRAFT"
        }
    )
    
    # Add some sample values for the submission
    await prisma.formvalue.create(
        data={
            "submissionId": form_submission.id,
            "fieldId": owner_field.id,
            "value": "John Smith Publishing Ltd."
        }
    )
    
    await prisma.formvalue.create(
        data={
            "submissionId": form_submission.id,
            "fieldId": work_description_field.id,
            "value": "A novel titled 'The Midnight Shadows' authored by Jane Smith"
        }
    )
    
    await prisma.formvalue.create(
        data={
            "submissionId": form_submission.id,
            "fieldId": copies_count_field.id,
            "value": "500"
        }
    )
    
    # Create another sample submission (SUBMITTED status)
    complete_submission = await prisma.formsubmission.create(
        data={
            "formId": copyright_form.id,
            "userId": admin_user.id,
            "status": "SUBMITTED"
        }
    )
    
    # Add complete values for the submission
    sample_values = {
        owner_field.id: "Acme Publishing House",
        work_description_field.id: "A technical manual titled 'Advanced Database Systems'",
        copies_count_field.id: "1000",
        arrival_time_field.id: "2025-04-15T10:00:00.000Z",
        arrival_place_field.id: "Mumbai Port",
        detention_period_field.id: "30",
        name_address_field.id: "Rajesh Kumar, 123 Business Park, New Delhi, India",
        work_class_field.id: "Literary",
        work_title_field.id: "Advanced Database Systems",
        author_details_field.id: "Dr. Priya Singh, 456 Tech Avenue, Bangalore, India, Indian",
        work_language_field.id: "English",
        publisher_field.id: "Acme Publishing House, 789 Publishing Row, Chennai, India",
        first_pub_year_field.id: "2023",
        first_pub_country_field.id: "India",
        registration_num_field.id: "CR-2023-45678",
        origin_country_field.id: "Malaysia",
        importer_details_field.id: "XYZ Importers, 101 Import Plaza, Kolkata, India, Indian",
        maker_details_field.id: "Counterfeit Books Ltd., 202 Fake Street, Kuala Lumpur, Malaysia, Malaysian",
        identify_willingness_field.id: "true",
        fee_payment_field.id: "Bank Draft No. BD12345678",
        additional_info_field.id: "The infringing copies have been spotted at the manufacturer's warehouse and are scheduled for shipping next week.",
        upload_work_copy_field.id: "original_work.pdf",
        upload_ownership_evidence_field.id: "copyright_certificate.pdf",
        upload_infringement_evidence_field.id: "comparison_analysis.pdf",
        upload_import_evidence_field.id: "shipping_documents.pdf",
        upload_fee_evidence_field.id: "bank_draft_receipt.pdf"
    }
    
    for field_id, value in sample_values.items():
        await prisma.formvalue.create(
            data={
                "submissionId": complete_submission.id,
                "fieldId": field_id,
                "value": value
            }
        )

    # ======================= FORM XIV (COPYRIGHT REGISTRATION) FIELDS =======================
    
    # Create fields for Form XIV - Application for Registration of Copyright
    applicant_name_field = await prisma.formfield.create(
        data={
            "label": "Applicant Name",
            "description": "Full name of the applicant applying for copyright registration",
            "fieldType": "TEXT",
            "isRequired": True,
            "validations": json.dumps({"minLength": 3, "maxLength": 200})
        }
    )
    
    applicant_address_field = await prisma.formfield.create(
        data={
            "label": "Applicant Address",
            "description": "Complete address of the applicant",
            "fieldType": "TEXTAREA",
            "isRequired": True,
            "validations": json.dumps({"minLength": 10, "maxLength": 500})
        }
    )
    
    applicant_nationality_field = await prisma.formfield.create(
        data={
            "label": "Applicant Nationality",
            "description": "Nationality of the applicant",
            "fieldType": "TEXT",
            "isRequired": True,
            "validations": json.dumps({"minLength": 2, "maxLength": 100})
        }
    )
    
    applicant_category_field = await prisma.formfield.create(
        data={
            "label": "Applicant Category",
            "description": "Category of the applicant",
            "fieldType": "SELECT",
            "isRequired": True,
            "validations": json.dumps({
                "options": ["Individual", "Business", "Others"]
            })
        }
    )
    
    communication_name_field = await prisma.formfield.create(
        data={
            "label": "Communication Name",
            "description": "Name of person to whom communications should be addressed",
            "fieldType": "TEXT",
            "isRequired": True,
            "validations": json.dumps({"minLength": 3, "maxLength": 200})
        }
    )
    
    communication_address_field = await prisma.formfield.create(
        data={
            "label": "Communication Address",
            "description": "Address where communications regarding registration should be sent",
            "fieldType": "TEXTAREA",
            "isRequired": True,
            "validations": json.dumps({"minLength": 10, "maxLength": 1024})
        }
    )
    
    communication_pincode_field = await prisma.formfield.create(
        data={
            "label": "Communication Pincode",
            "description": "Postal code for the communication address",
            "fieldType": "TEXT",
            "isRequired": False,
            "validations": json.dumps({"pattern": "^[0-9]{6}$", "maxLength": 6})
        }
    )
    
    communication_phone_field = await prisma.formfield.create(
        data={
            "label": "Communication Phone",
            "description": "Phone number for communication purposes",
            "fieldType": "TEXT",
            "isRequired": False,
            "validations": json.dumps({"pattern": "^[0-9]{10,12}$", "maxLength": 12})
        }
    )
    
    registration_work_title_field = await prisma.formfield.create(
        data={
            "label": "Title of Work",
            "description": "Title of the work for which copyright registration is sought",
            "fieldType": "TEXT",
            "isRequired": True,
            "validations": json.dumps({"minLength": 1, "maxLength": 200})
        }
    )
    
    registration_work_description_field = await prisma.formfield.create(
        data={
            "label": "Description of Work",
            "description": "Brief description of the work",
            "fieldType": "TEXTAREA",
            "isRequired": True,
            "validations": json.dumps({"minLength": 10, "maxLength": 500})
        }
    )
    
    registration_work_class_field = await prisma.formfield.create(
        data={
            "label": "Class of Work",
            "description": "Category of work for which copyright registration is sought",
            "fieldType": "SELECT",
            "isRequired": True,
            "validations": json.dumps({
                "options": ["Literary", "Dramatic", "Musical", "Artistic", "Cinematograph Film", "Sound Recording", "Computer Software"]
            })
        }
    )
    
    registration_work_language_field = await prisma.formfield.create(
        data={
            "label": "Language of Work",
            "description": "Language in which the work is expressed (especially for literary works and computer software)",
            "fieldType": "TEXT",
            "isRequired": True,
            "validations": json.dumps({"minLength": 2, "maxLength": 50})
        }
    )
    
    author_name_field = await prisma.formfield.create(
        data={
            "label": "Author Name",
            "description": "Full name of the author of the work",
            "fieldType": "TEXT",
            "isRequired": True,
            "validations": json.dumps({"minLength": 3, "maxLength": 200})
        }
    )
    
    author_address_field = await prisma.formfield.create(
        data={
            "label": "Author Address",
            "description": "Address of the author",
            "fieldType": "TEXTAREA",
            "isRequired": True,
            "validations": json.dumps({"minLength": 10, "maxLength": 500})
        }
    )
    
    author_nationality_field = await prisma.formfield.create(
        data={
            "label": "Author Nationality",
            "description": "Nationality of the author",
            "fieldType": "TEXT",
            "isRequired": True,
            "validations": json.dumps({"minLength": 2, "maxLength": 100})
        }
    )
    
    deceased_author_date_field = await prisma.formfield.create(
        data={
            "label": "Date of Author's Decease",
            "description": "If the author is deceased, the date of death",
            "fieldType": "DATE",
            "isRequired": False,
            "validations": json.dumps({})
        }
    )
    
    work_published_status_field = await prisma.formfield.create(
        data={
            "label": "Publication Status",
            "description": "Is the work published or unpublished",
            "fieldType": "SELECT",
            "isRequired": True,
            "validations": json.dumps({
                "options": ["Published", "Unpublished"]
            })
        }
    )
    
    publisher_name_field = await prisma.formfield.create(
        data={
            "label": "Publisher Name",
            "description": "Name of the publisher",
            "fieldType": "TEXT",
            "isRequired": False,
            "validations": json.dumps({"minLength": 3, "maxLength": 200})
        }
    )
    
    publisher_address_field = await prisma.formfield.create(
        data={
            "label": "Publisher Address",
            "description": "Address of the publisher",
            "fieldType": "TEXTAREA",
            "isRequired": False,
            "validations": json.dumps({"minLength": 10, "maxLength": 500})
        }
    )
    
    publication_year_field = await prisma.formfield.create(
        data={
            "label": "Year of First Publication",
            "description": "Year when the work was first published",
            "fieldType": "NUMBER",
            "isRequired": False,
            "validations": json.dumps({"min": 1800, "max": 2025})
        }
    )
    
    publication_country_field = await prisma.formfield.create(
        data={
            "label": "Country of First Publication",
            "description": "Country where the work was first published",
            "fieldType": "TEXT",
            "isRequired": False,
            "validations": json.dumps({"minLength": 2, "maxLength": 100})
        }
    )
    
    copyright_owners_field = await prisma.formfield.create(
        data={
            "label": "Copyright Owners",
            "description": "Names, addresses and nationalities of owners of various rights comprising the copyright",
            "fieldType": "TEXTAREA",
            "isRequired": True,
            "validations": json.dumps({"minLength": 10, "maxLength": 500})
        }
    )
    
    is_original_work_field = await prisma.formfield.create(
        data={
            "label": "Is Original Work",
            "description": "Is this an original work (not an adaptation or translation)",
            "fieldType": "CHECKBOX",
            "isRequired": True,
            "validations": json.dumps({})
        }
    )
    
    artistic_work_location_field = await prisma.formfield.create(
        data={
            "label": "Artistic Work Location",
            "description": "For artistic works, the location of the original work",
            "fieldType": "TEXT",
            "isRequired": False,
            "validations": json.dumps({"minLength": 0, "maxLength": 200})
        }
    )
    
    declaration_field = await prisma.formfield.create(
        data={
            "label": "Declaration",
            "description": "I verify that particulars given in this form are true to the best of my knowledge",
            "fieldType": "CHECKBOX",
            "isRequired": True,
            "validations": json.dumps({})
        }
    )
    
    fee_payment_details_field = await prisma.formfield.create(
        data={
            "label": "Fee Payment Details",
            "description": "Details of payment of registration fee",
            "fieldType": "TEXT",
            "isRequired": True,
            "validations": json.dumps({"minLength": 5, "maxLength": 100})
        }
    )
    
    upload_work_sample_field = await prisma.formfield.create(
        data={
            "label": "Work Sample",
            "description": "Upload a sample or copy of the work for which registration is sought",
            "fieldType": "FILE",
            "isRequired": True,
            "validations": json.dumps({"fileTypes": ["pdf", "docx", "jpg", "png"], "maxSize": 10})
        }
    )
    
    upload_signature_field = await prisma.formfield.create(
        data={
            "label": "Applicant Signature",
            "description": "Upload applicant's signature (jpg/jpeg, less than 512KB)",
            "fieldType": "FILE",
            "isRequired": True,
            "validations": json.dumps({"fileTypes": ["jpg", "jpeg"], "maxSize": 0.5})
        }
    )
    
    # Create Form XIV for Copyright Registration
    # Generate a random embedding vector of dimension 1024
    
    registration_form_description = """
    FORM XIV - APPLICATION FOR REGISTRATION OF COPYRIGHT [SEE RULE 70]
    For applying to the Registrar of Copyrights, Copyright Office, New Delhi for registration of copyright
    in accordance with section 45 of the Copyright Act, 1957 (14 of 1957).
    """
    registration_embedding_vector = generate_form_embeddings(name="FORM XIV - APPLICATION FOR REGISTRATION OF COPYRIGHT [SEE RULE 70]",description=registration_form_description)
    
    copyright_registration_form = await prisma.form.create(
        data={
            "title": "Form XIV - Application for Registration of Copyright",
            "description": registration_form_description,
            "embeddings": registration_embedding_vector,
        }
    )
    
    # Associate fields with Form XIV
    reg_field_order = 1
    for field in [
        applicant_name_field,
        applicant_address_field,
        applicant_nationality_field,
        applicant_category_field,
        registration_work_title_field,
        registration_work_description_field,
        registration_work_class_field,
        registration_work_language_field,
        author_name_field,
        author_address_field,
        author_nationality_field,
        deceased_author_date_field,
        work_published_status_field,
        publisher_name_field,
        publisher_address_field,
        publication_year_field,
        publication_country_field,
        copyright_owners_field,
        is_original_work_field,
        artistic_work_location_field,
        communication_name_field,
        communication_address_field,
        communication_pincode_field,
        communication_phone_field,
        declaration_field,
        fee_payment_details_field,
        upload_work_sample_field,
        upload_signature_field
    ]:
        await prisma.formfieldonform.create(
            data={
                "formId": copyright_registration_form.id,
                "fieldId": field.id,
                "order": reg_field_order
            }
        )
        reg_field_order += 1
    
    # Create a sample form submission for Form XIV (DRAFT status)
    reg_form_submission = await prisma.formsubmission.create(
        data={
            "formId": copyright_registration_form.id,
            "userId": regular_user.id,
            "status": "DRAFT"
        }
    )
    
    # Add some sample values for the registration submission
    await prisma.formvalue.create(
        data={
            "submissionId": reg_form_submission.id,
            "fieldId": applicant_name_field.id,
            "value": "SARVESH DAKHORE"
        }
    )
    
    await prisma.formvalue.create(
        data={
            "submissionId": reg_form_submission.id,
            "fieldId": registration_work_title_field.id,
            "value": "Digital Innovation Framework"
        }
    )
    
    await prisma.formvalue.create(
        data={
            "submissionId": reg_form_submission.id,
            "fieldId": registration_work_class_field.id,
            "value": "Literary"
        }
    )
    
    await prisma.formvalue.create(
        data={
            "submissionId": reg_form_submission.id,
            "fieldId": communication_address_field.id,
            "value": "CDS"
        }
    )
    
    # Create a complete submission for Form XIV (SUBMITTED status)
    reg_complete_submission = await prisma.formsubmission.create(
        data={
            "formId": copyright_registration_form.id,
            "userId": admin_user.id,
            "status": "SUBMITTED"
        }
    )
    
    # Add complete values for the registration submission
    reg_sample_values = {
        applicant_name_field.id: "Tech Innovations Pvt Ltd",
        applicant_address_field.id: "123 Innovation Park, Bengaluru, Karnataka, India",
        applicant_nationality_field.id: "Indian",
        applicant_category_field.id: "Business",
        registration_work_title_field.id: "AI-Powered Data Analytics Platform",
        registration_work_description_field.id: "A comprehensive software solution for data analytics using artificial intelligence and machine learning algorithms",
        registration_work_class_field.id: "Computer Software",
        registration_work_language_field.id: "English, Python",
        author_name_field.id: "Rahul Sharma",
        author_address_field.id: "456 Tech Valley, Bengaluru, Karnataka, India",
        author_nationality_field.id: "Indian",
        work_published_status_field.id: "Published",
        publisher_name_field.id: "Tech Innovations Pvt Ltd",
        publisher_address_field.id: "123 Innovation Park, Bengaluru, Karnataka, India",
        publication_year_field.id: "2024",
        publication_country_field.id: "India",
        copyright_owners_field.id: "Tech Innovations Pvt Ltd, 123 Innovation Park, Bengaluru, Karnataka, India, Indian - All Rights Reserved",
        is_original_work_field.id: "true",
        communication_name_field.id: "Rahul Sharma",
        communication_address_field.id: "456 Tech Valley, Bengaluru, Karnataka, India",
        communication_pincode_field.id: "560001",
        communication_phone_field.id: "9876543210",
        declaration_field.id: "true",
        fee_payment_details_field.id: "Payment ID: COPY-REG-2024-78901",
        upload_work_sample_field.id: "software_documentation.pdf",
        upload_signature_field.id: "sharma_signature.jpg"
    }
    
    for field_id, value in reg_sample_values.items():
        await prisma.formvalue.create(
            data={
                "submissionId": reg_complete_submission.id,
                "fieldId": field_id,
                "value": value
            }
        )
    
    print("Database seeded successfully!")
    
    # Disconnect from the database
    await prisma.disconnect()

# Run the async function
import asyncio
asyncio.run(main())