# save_it.py
def save_func(final_uris, output, domain):
    # Tentukan nama file output jika tidak diberikan
    if not output:
        output = f'output/{domain}.txt'
    
    # Menyimpan hasil ke file
    with open(output, 'w') as f:
        for uri in final_uris:
            f.write(f"{uri}\n")
    
    print(f"Hasil telah disimpan di: {output}")
