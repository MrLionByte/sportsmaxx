import re

# Create your views here.
name_regex = r"^[a-zA-Z0-9\s-]*$"
email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
username_regex = r"^[A-Za-z][A-Za-z0-9_]{5,29}$"
first_last_name_regex = r"^[A-Za-z\s'-]+$"
email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
percentage_regex = r"^\d+(\.\d{1,2})?$"
color_regex = (r"^[a-z\s-]+$",)
variant_regex = r"^[A-Za-z0-9\s_-]+$"
pin_regex = r"^\d{6}$"
post_office_regex = r"^[a-zA-Z0-9\s\-\(\)]+$"
phone_regex = r"^(9|8|7)\d{9}$"
city_regex = r"^[a-zA-Z\s\-\(\)]+$"
area_regex = r"^[a-zA-Z0-9\s,\.\-]+$"
landmark_regex = r"^[a-zA-Z0-9\s,.\-]+$"
couponcode_regex = r"^[A-Z0-9]+$"


indian_states_and_ut = [
    "Andhra Pradesh",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Chhattisgarh",
    "Goa",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Madhya Pradesh",
    "Maharashtra",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odisha",
    "Punjab",
    "Rajasthan",
    "Sikkim",
    "Tamil Nadu",
    "Telangana",
    "Tripura",
    "Uttar Pradesh",
    "Uttarakhand",
    "West Bengal",
    "Andaman and Nicobar Islands",
    "Chandigarh",
    "Dadra and Nagar Haveli and Daman and Diu",
    "Delhi",
    "Lakshadweep",
    "Puducherry",
    "Ladakh",
    "Jammu and Kashmir",
]


def is_image(filename):
    lowercase_filename = filename.lower()
    allowed_extensions = [".jpg", ".jpeg", ".png"]
    return any(lowercase_filename.endswith(ext) for ext in allowed_extensions)


def username_test(username):
    if not username.strip():
        message = "Username cannot be empty or just whitespace"
        return True, message
    if not re.match(username_regex, username):
        message = "Username must start with a letter, be 6-30 characters long, and contain only letters, numbers, and underscores"
        return True, message
    if username != username.strip():
        message = "Do not use unwanted spaces"
        return True, message

    return False, "Username is valid"


def name_validator(firstOrLast_name):
    if not firstOrLast_name.strip():
        message = "Name cannot be empty"
        return True, message
    if len(firstOrLast_name) < 3:
        message = "Name must have at least 3 character"
        return True, message
    if len(firstOrLast_name) > 50:
        message = "Name must not exceed 50 characters"
        return True, message
    if firstOrLast_name != firstOrLast_name.strip():
        message = "Name should not have unwanted spaces"
        return True, message
    if "  " in firstOrLast_name:
        message = "Name should not contain unwanted spaces"
        return True, message
    if not re.match(first_last_name_regex, firstOrLast_name):
        message = "Name can only contain letters, spaces"
        return True, message
    if not firstOrLast_name[0].isalpha() or not firstOrLast_name[1].isalpha():
        message = "Name can only contain Alphabets"
        return True, message

    return False, "Name is valid"


def email_test(email):
    if not email.strip():
        message = "Email cannot be empty"
        return True, message
    if not re.match(email_regex, email):
        message = "Invalid email format"
        return True, message
    if len(email) > 256:
        message = "Email must not exceed 256 characters"
        return True, message
    if len(email) < 5:
        message = "Email must be at least 5 characters long"
        return True, message
    if email != email.strip():
        message = "Email should not have unwanted spaces"
        return True, message

    return False, "Email is valid"


def name_test(categoryname):
    if not categoryname.strip():
        message = "Name cannot be empty or just whitespace"
        return True, message
    if len(categoryname) < 4:
        message = "Make sure name has min 4 letters, (min 4)"
        return True, message
    if len(categoryname) > 40:
        message = "Exceeds the valid name length, (max 40)"
        return True, message
    if categoryname != categoryname.strip():
        return True, "Don't use unwanted spaces"
    if "  " in categoryname:
        message = "Don't use unwanted spaces"
        return True, message
    alpha = categoryname[0].isalpha()
    if not alpha:
        message = "Name should start with a Alphabet"
        return True, message
    lowercase_categoryname = categoryname.lower()
    if (
        lowercase_categoryname[0]
        == lowercase_categoryname[1]
        == lowercase_categoryname[2]
    ):
        message = "Give a valid category name without repeated "
        message += "characters in beginning"
        return True, message
    elif not re.match(name_regex, categoryname):
        message = "Don't use invalid characters  "
        message += "(only letters, numbers, spaces, and hyphens are allowed)"
        return True, message

    return False, "Name is valid"


def price_test(price):
    try:
        price = int(price)
        if price <= 0:
            return True, "Price must be greater than zero"
        if price > 100000:
            return True, "Price exceeds the maximum limit of 1,00,000"
        if not re.match(r"^\d+(\.\d{1,2})?$", str(price)):
            return True, "Price can have at most two decimal places"

        return False, "Price is valid"
    except TypeError:
        price = float(price)
    except ValueError:
        price = float(price)
    if price <= 0:
        return True, "Price must be greater than zero"
    if price > 100000:
        return True, "Price exceeds the maximum limit of 1,00,000"
    if not re.match(r"^\d+(\.\d{1,2})?$", str(price)):
        return True, "Price can have at most two decimal places"

    return False, "Price is valid"


def percentage_validator(percentage):
    try:
        percentage = float(percentage)
    except ValueError:
        return True, "Percentage must be a number"
    if percentage < 0 or percentage > 90:
        return True, "Percentage must be between 0 and 90"
    if not re.match(percentage_regex, str(percentage)):
        return True, "Percentage can have at most two decimal places"

    return False, "Percentage is valid"


def description_validator(description):
    if not description.strip():
        return True, "Description cannot be empty or just whitespace"
    if len(description) < 5:
        return True, "Description must have at least 10 characters"
    if len(description) > 2000:
        return True, "Description must not exceed 2000 characters"
    if re.search(r"\s{2,}", description):
        return True, "Description should not contain  unwanted spaces"
    if not re.match(r'^[\w\s.,!\'"()-]*$', description):
        return True, "Description contains invalid characters"
    if re.search(r"<[^>]*>", description):
        return True, "Description should not contain HTML tags"

    return False, "Description is valid"


def color_validator(color):
    if not color.strip():
        message = "Color cannot be empty"
        return True, message
    color = color.strip().lower()
    if len(color) < 3 or len(color) > 20:
        message = "Color name must be between 3 and 30 characters"
        return True, message
    if not re.match(r"^[a-z\s-]+$", color):
        message = "Invalid characters detected"
        return True, message
    if color != color.strip():
        message = "Color name should not have unwanted spaces"
        return True, message
    if "  " in color:
        message = "Color name should not contain unwanted spaces"
        return True, message
    if color[0] == color[1] == color[2]:
        message = "Give valid color name"
        return True, message

    return False, "Color name is valid"


def variant_validator(variant_name):
    if not variant_name.strip():
        message = "Variant name cannot be empty"
        return True, message
    variant_name = variant_name.strip()
    if len(variant_name) < 3 or len(variant_name) > 50:
        message = "Variant name must be between 3 and 50 characters long"
        return True, message
    if not re.match(variant_regex, variant_name):
        message = "Variant name contains invalid characters."
        return True, message
    if variant_name != variant_name.strip():
        message = "Variant name should not have unwanted spaces"
        return True, message
    if "  " in variant_name:
        message = "Variant name should not have unwanted spaces"
        return True, message

    return False, "Variant name is valid"


def product_quantity_validator(quantity):
    if quantity is None:
        message = "Quantity cannot be empty"
        return True, message
    if not isinstance(quantity, (int, float, str)) or not str(quantity).isdigit():
        message = "Quantity must be a numeric value"
        return True, message
    quantity = int(quantity)
    if not isinstance(quantity, int):
        message = "Quantity must be an integer"
        return True, message
    if quantity < 0:
        message = "Quantity cannot be negative"
        return True, message
    if quantity > 10000:
        message = "Quantity cannot exceed 10000"
        return True, message
    if quantity < 1:
        message = "Quantity must be at least 1"
        return True, message

    return False, "Quantity is valid"


def validate_pin_code(pin_code):
    if not pin_code:
        message = "PIN code cannot be empty."
        return True, message
    if not re.match(pin_regex, pin_code):
        message = "Invalid PIN code format. It should be a 6-digit number."
        return True, message
    message = "PIN code is valid."

    return False, message


def validate_post_office_name(post_office):
    if not post_office:
        message = "Post office name cannot be empty."
        return True, message
    if not re.match(post_office_regex, post_office):
        message = "Invalid post office name format."
        return True, message
    message = "Post office name is valid."

    return False, message


def validate_phone(phone):
    if not phone:
        message = "Phone number cannot be empty."
        return True, message
    if not re.match(phone_regex, phone):
        message = "Invalid phone number format."
        return True, message
    if len(phone) != 10:
        message = "Make phone number have 10 digits."
        return True, message
    message = "Phone number is valid."

    return False, message


def validate_state(state):
    state = state.upper()[0] + state.lower()[1:]
    if not state:
        message = "State name cannot be empty."
        return True, message
    if state in indian_states_and_ut:
        message = "State name is valid."
        return False, message
    else:
        message = "Invalid state name."
        return True, message


def validate_city(city):
    if not city:
        message = "City name cannot be empty."
        return True, message
    if re.search(r"\s{2,}", city) or re.search(r",,{2,}", city):
        message = "City name cannot contain multiple consecutive spaces or commas."
        return True, message
    if re.search(r"(.)\1{6,}", city):
        message = "Area name cannot contain a single character repeated more than 6 times consecutively."
        return True, message
    if re.match(city_regex, city):
        message = "City name is valid."
        return False, message
    else:
        message = "Invalid city name format."
        return True, message


def validate_area(area):
    min_length = 3
    max_length = 50
    if not area:
        message = "Area name cannot be empty."
        return True, message
    if len(area) < min_length or len(area) > max_length:
        message = (
            f"Area name must be between {min_length} and {max_length} characters long."
        )
        return True, message
    if re.search(r"\s{2,}", area) or re.search(r",,{2,}", area):
        message = "Area name cannot contain multiple consecutive spaces or commas."
        return True, message
    if not re.match(area_regex, area):
        message = "Invalid area name format. It should contain only letters, numbers, spaces, hyphens, commas, and periods."
        return True, message
    if re.search(r"(.)\1{6,}", area):
        message = "Area name cannot contain a single character repeated more than 6 times consecutively."
        return True, message

    message = "Area name is valid."
    return False, message


def validate_landmark(landmark):
    if not landmark:
        message = "No landmark provided."
        return True, message
    if len(landmark) < 2 or len(landmark) > 100:
        message = "Landmark length should be between 2 and 100 characters."
        return True, message
    if not re.match(landmark_regex, landmark):
        message = "Invalid landmark format."
        return True, message

    message = "Landmark is valid."
    return False, message


def validate_password(password):
    if len(password) < 8:
        message = "Password must be at least 8 characters long."
        return True, message
    if len(password) > 64:
        message = "Password cannot exceed 64 characters."
        return True, message
    if not re.search(r"[A-Z]", password):
        message = "Password must contain at least one uppercase letter."
        return True, message
    if not re.search(r"[a-z]", password):
        message = "Password must contain at least one lowercase letter."
        return True, message
    if not re.search(r"\d", password):
        message = "Password must contain at least one digit."
        return True, message
    if not re.search(r"[!@#$%^&*()\-_=+{}[\]|\\;:'\",<.>/?]", password):
        message = "Password must contain at least one special character."
        return True, message
    if re.search(r"\s", password):
        message = "Password cannot contain whitespace characters."
        return True, message

    message = "Password is valid."
    return False, message


def couponcode_validate(code):
    if not re.match(couponcode_regex, code):
        message = "Coupon code should only contain alphabets and numbers."
        return True, message

    message = "Valid coupon code"
    return False, message
