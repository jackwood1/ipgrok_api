# config.py

base_matching_attribs = [
    "last name",
    "first name",
    "dob"
]

extended_bases_attribs = [
    "gender",
    "salary"
]

enrollment_fields = {
    "Name": ["full name", "name"],
    "Last Name": ["last name", "name"],
    "First Name": ["first name", "name"],
    "Birth Date": ["dob", "date"],
    "Gender": ["gender", "gender"],
    "Occupation": ["occupation", "string"],
    "Bill Location": ["bill location", "string"],
    "Annual Salary": ["salary", "currency"],
    "Termination Date": ["termination date", None],
    "Basic Employee AD&D Benefit": ["basic employee add benefit", "currency"],
    "Basic Employee AD&D Class #": ["basic employee add class", "string"],
    "Basic Employee AD&D Effective Date": ["basic employee add effective date", "date"],
    "Basic Employee Life Benefit": ["basic employee life benefit", "currency"],
    "Basic Employee Life Class #": ["basic employee life class", "string"],
    "Basic Employee Life Effective Date": ["basic employee life effective date", "date"],
    "Long Term Disability Benefit": ["long term disability benefit", "currency"],
    "Long Term Disability Class #": ["long term disability class", "string"],
    "Long Term Disability Effective Date": ["long term disability effective date", "date"],
    "Short Term Disability Benefit": ["short term disability benefit", "currency"],
    "Short Term Disability Class #": ["short term disability class", "string"],
    "Short Term Disability Effective Date": ["short term disability effective date", "date"],
    "Supplemental Child AD&D Benefit": ["supplemental child add benefit", "currency"],
    "Supplemental Child AD&D Class #": ["supplemental child add class", "string"],
    "Supplemental Child AD&D Effective Date": ["supplemental child add effective date", "date"],
    "Supplemental Child Life Benefit": ["supplemental child life benefit", "currency"],
    "Supplemental Child Life Class #": ["supplemental child life class", "string"],
    "Supplemental Child Life Effective Date": ["supplemental child life effective date", "date"],
    "Supplemental Employee AD&D Benefit": ["supplemental employee add benefit", "currency"],
    "Supplemental Employee AD&D Class #": ["supplemental employee add class", "string"],
    "Supplemental Employee AD&D Effective Date": ["supplemental employee add effective date", "date"],
    "Supplemental Employee Life Benefit": ["supplemental employee life benefit", "currency"],
    "Supplemental Employee Life Class #": ["supplemental employee life class", "string"],
    "Supplemental Employee Life Effective Date": ["supplemental employee life effective date", "date"],
    "Supplemental Spouse AD&D Benefit": ["supplemental spouse add benefit", "currency"],
    "Supplemental Spouse AD&D Class #": ["supplemental spouse add class", "string"],
    "Supplemental Spouse AD&D Effective Date": ["supplemental spouse add effective date", "date"],
    "Supplemental Spouse Life Benefit": ["supplemental spouse life benefit", "currency"],
    "Supplemental Spouse Life Class #": ["supplemental spouse life class", "string"],
    "Supplemental Spouse Life Effective Date": ["supplemental spouse life effective date", "date"]
}

core_product_names = [
    "basic employee life",
    "basic employee add",
    "supplemental employee life",
    "supplemental spouse life",
    "supplemental child life",
    "supplemental employee add",
    "supplemental child add",
    "short term disability",
    "long term disability"
]

core_product_attribs = [
    "benefit",
    "class",
    "effective date"
]

partner_product_names = [
    "Basic Life",
    "Basic ADD",
    "Supplemental Life",
    "Supplemental Spouse Life",
    "Supplemental Child Life",
    "Supplemental ADD",
    "Supplemental Spouse ADD",
    "Supplemental Child ADD",
    "VSTD",
    "Long Term Disability"
]

partner_product_attrs = {
    "Class": "REPLACE class",
    "Class Change Effective Date": "REPLACE change effective date",
    "Coverage Amount": "REPLACE coverage amount",
    "Coverage Effective Date": "REPLACE coverage date",
    "Termination Date": "REPLACE termination date"
}


partner_fields = {
    "Status": ["status", None],
    "Action": ["action", None],
    "Last Name": ["last name", "name"],
    "First Name": ["first name", "name"],
    "Middle Initial": ["middle initial", "string"],
    "Gender": ["gender", "gender"],
    "Date of Birth": ["dob", "date"],
    "Date of Hire": ["date of hire", "date"],
    "Part time to Full Time Effective Date": ["conversion effective date", "date"],
    "Salary": ["salary", "currency"],
    "Salary Effective Date": ["salary effective date", "date"],
    "Division": ["division", None],
    "Change Date": ["change date", "date"],
    "Basic Life": ["basic employee life", "string"],
    "Basic Life class": ["basic employee life class", "string"],
    "Basic Life change effective date": ["basic employee life effective date", "date"],
    "Basic Life coverage amount": ["basic employee life benefit", "currency"],
    "Basic Life coverage date": ["basic employee life coverage date", "date"],
    "Basic Life termination date": ["basic employee life termination date", "date"],
    "Basic ADD": ["basic employee add", "string"],
    "Basic ADD class": ["basic employee add class", "string"],
    "Basic ADD change effective date": ["basic employee add effective date", "date"],
    "Basic ADD coverage amount": ["basic employee add benefit", "currency"],
    "Basic ADD coverage date": ["basic employee add coverage date", "date"],
    "Basic ADD termination date": ["basic employee add termination date", "date"],
    "Supplemental Life": ["supplemental employee life", "string"],
    "Supplemental Life class": ["supplemental employee life class", "string"],
    "Supplemental Life change effective date": ["supplemental employee life effective date", "date"],
    "Supplemental Life coverage amount": ["supplemental employee life benefit", "currency"],
    "Supplemental Life coverage date": ["supplemental employee life coverage date", "date"],
    "Supplemental Life termination date": ["supplemental employee life termination date", "date"],
    "Spouse Date of Birth": ["supplemental spouse life benefit dob", "string"],
    "Supplemental Spouse Life": ["supplemental spouse life", "currency"],
    "Supplemental Spouse Life class": ["supplemental spouse life class", "string"],
    "Supplemental Spouse Life change effective date": ["supplemental spouse life effective date", "date"],
    "Supplemental Spouse Life coverage amount": ["supplemental spouse life benefit", "currency"],
    "Supplemental Spouse Life coverage date": ["supplemental spouse life coverage date", "date"],
    "Supplemental Spouse Life termination date": ["supplemental spouse life termination date", "date"],
    "Supplemental Child Life": ["supplemental child life", "string"],
    "Supplemental Child Life class": ["supplemental child life class", "string"],
    "Supplemental Child Life change effective date": ["supplemental child life effective date", "date"],
    "Supplemental Child Life coverage amount": ["supplemental child life benefit", "currency"],
    "Supplemental Child Life coverage date": ["supplemental child life coverage date", "date"],
    "Supplemental Child Life termination date": ["supplemental child life termination date", "date"],
    "Supplemental ADD": ["supplemental employee add", "currency"],
    "Supplemental ADD class": ["supplemental employee add class", "string"],
    "Supplemental ADD change effective date": ["supplemental employee add effective date", "date"],
    "Supplemental ADD coverage amount": ["supplemental employee add benefit", "currency"],
    "Supplemental ADD coverage date": ["supplemental employee add coverage date", "date"],
    "Supplemental ADD termination date": ["supplemental employee add termination date", "date"],
    "Supplemental Spouse ADD": ["supplemental spouse add", "currency"],
    "Supplemental Spouse ADD class": ["supplemental spouse add class", "string"],
    "Supplemental Spouse ADD change effective date": ["supplemental spouse add effective date", "date"],
    "Supplemental Spouse ADD coverage amount": ["supplemental spouse add benefit", "currency"],
    "Supplemental Spouse ADD coverage date": ["supplemental spouse add coverage date", "date"],
    "Supplemental Spouse ADD termination date": ["supplemental spouse add termination date", "date"],
    "Supplemental Child ADD": ["supplemental child add", "currency"],
    "Supplemental Child ADD class": ["supplemental child add class", "string"],
    "Supplemental Child ADD change effective date": ["supplemental child add effective date", "date"],
    "Supplemental Child ADD coverage amount": ["supplemental child add benefit", "currency"],
    "Supplemental Child ADD coverage date": ["supplemental child add coverage date", "date"],
    "Supplemental Child ADD termination date": ["supplemental child add termination date", "date"],
    "VSTD": ["short term disability", "string"],
    "VSTD class": ["short term disability class", "string"],
    "VSTD change effective date": ["short term disability effective date", "date"],
    "VSTD coverage amount": ["short term disability benefit", "currency"],
    "VSTD coverage date": ["short term disability coverage date", "date"],
    "VSTD termination date": ["short term disability termination date", "date"],
    "Long Term Disability": ["long term disability", "srting"],
    "Long Term Disability class": ["long term disability class", "string"],
    "Long Term Disability change effective date": ["long term disability effective date", "date"],
    "Long Term Disability coverage amount": ["long term disability benefit", "currency"],
    "Long Term Disability coverage date": ["long term disability coverage date", "date"],
    "Long Term Disability termination date": ["long term disability termination date", "date"],
}

sort_fixed_columns = [
    'first name',
    'last name',
    'change',
    'full name',
    'status',
    'action',
    'change date',
    'dob',
    'date of hire',
    'salary effective date'
]

sort_match_columns = [
     'salary.*',
     'gender.*'
 ]

drop_columns = [
    'division',
    'occupation',
    'conversion effective date',
    'bill location',
    '_merge'
]
