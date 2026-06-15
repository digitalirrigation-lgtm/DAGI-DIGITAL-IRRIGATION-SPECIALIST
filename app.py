service_account = st.secrets["service_account"]

credentials = ee.ServiceAccountCredentials(
    service_account,
    key_data=st.secrets["private_key"]
)

ee.Initialize(credentials)
