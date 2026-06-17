from time import perf_counter

def normalize_name(value):
    return " ".join(str(value).strip().split())

def parse_decimal(value):
    if value is None:
        return 0.0
    
    text = str(value).strip()
    if not text:
        return 0.0
    
    return float(text.replace(".","").replace(",","."))

def format_rupiah(value):
    return "Rp {:,.2f}".format(value).replace(",","X").replace(".",",").replace("X",".")

def format_route(route):
    return "-->".join(route)

def measure_time_ms(function,*args,**kwargs):
    start = perf_counter()
    result = function(*args,**kwargs)
    end = perf_counter()
    return result, (end-start) * 1000

def group_package_weight_by_destination(packages):
    weights = {}

    for package in packages:
        destination = normalize_name(package["destination"])
        weight = float(package["weight_kg"])
        weights[destination] = weights.get(destination, 0.0) + weight

    return weights

def validate_required_columns(file_name, row, required_columns):
    missing = [column for column in required_columns if column not in row]

    if missing:
        raise ValueError(f"File {file_name} tidak memiliki kolom wajib : {', '.join(missing)}")
    
