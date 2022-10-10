import secrets


def generate_vanity(min_length, max_length):
    """Generate a random string of length between min_length and max_length."""
    length = secrets.choice(range(min_length, max_length))
    choices = "abcdefghijklmnopqrstuvwxyz1234567890"
    vanity = ""

    for _ in range(0, length):
        vanity += choices[secrets.choice(range(0, len(choices)))]
    return vanity


def generate_unique_vanity(min_length, max_length, model):
    """Generate a unique random string of length between min_length and max_length."""
    vanity = generate_vanity(min_length, max_length)

    if model.objects.filter(slug=vanity).exists():
        return generate_unique_vanity(min_length, max_length, model)
    return vanity
