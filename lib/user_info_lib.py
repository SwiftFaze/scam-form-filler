import names
from faker import Faker

fake_fr = Faker('fr_FR')
def generate_random_person():
    person = {
        'first_name': names.get_first_name(),
        'last_name': names.get_last_name(),
    }
    person['full_name'] = person['first_name'] + " " + person['last_name']
    
    dob_day = str(fake_fr.day_of_month())
    dob_month = str(fake_fr.month())
    dob_year = str(fake_fr.year())
    person.update({
        'dob_day': dob_day,
        'dob_month': dob_month,
        'dob_year': dob_year,
        'dob': dob_day + "/" + dob_month + "/" + dob_year,
        'address': fake_fr.address(),
        'city': fake_fr.city(),
        'street_address': fake_fr.street_address(),
        'postal_code': fake_fr.postcode(),
        'telephone': fake_fr.phone_number(),
        'email': fake_fr.free_email(),
        'bank_card_number': fake_fr.credit_card_number(card_type=None),
    })
    
    bank_card_month = fake_fr.credit_card_expire(start="now", end="+10y", date_format="%m")
    bank_card_year = fake_fr.credit_card_expire(start="now", end="+10y", date_format="%y")
    person.update({
        'bank_card_month': bank_card_month,
        'bank_card_year': bank_card_year,
        'bank_card_expiration': bank_card_month + "/" + bank_card_year,
        'bank_card_cvv': fake_fr.credit_card_security_code(card_type=None)
    })
    person['user_agent'] = fake_fr.user_agent()
    return person



