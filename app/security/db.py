
# FAKE USER DATABASE
# IN REALITY, STORED IN A PLAINTEXT FILE (JSON? TOML?)

users = {
    "johndoe": {
        "name": "johndoe",
        "hash": "$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc",
    },
    "ahmad": {
        "name": "ahmad",
        "hash": "$argon2id$v=19$m=16,t=2,p=1$OGtQOVhGMDRtbWIxaFVrWA$bk3EZUx6wm1+NemBV1I8jQ",  # password is 'test'
    }
}
