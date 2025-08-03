import streamlit as st
import requests
import json
import pandas as pd

# ----------------- State-District Mapping ------------------
# This dictionary remains the same
state_district_map = {
    "Andaman And Nicobar": ["Nicobar", "North and Middle Andaman", "South Andaman"],
    "Andhra Pradesh": ["Anantapur", "Chittoor", "East Godavari", "Guntur", "Krishna", "Kurnool", "Nellore", "Prakasam", "Srikakulam", "Visakhapatnam", "Vizianagaram", "West Godavari", "Y S R Kadapa"],
    "Arunachal Pradesh": ["Anjaw", "Changlang", "Dibang Valley", "East Kameng", "East Siang", "Kamale", "Kra Daadi", "Kurung Kumey", "Lepa Rada", "Lohit", "Longding", "Lower Dibang Valley", "Lower Siang", "Lower Subansiri", "Namsai", "Pakke kessang", "Papum Pare", "Shi Yomi", "Siang", "Tawang", "Tirap", "Upper Siang", "Upper Subansiri", "West Kameng", "West Siang"],
    "Assam": ["Baksa", "Barpeta", "Bongaigaon", "Cachar", "Chirang", "Darrang", "Dhemaji", "Dhubri", "Dibrugarh", "Goalpara", "Golaghat", "Hailakandi", "Jorhat", "Kamrup Rural", "Karbi Anglong", "Karimganj", "Kokrajhar", "Lakhimpur", "Morigaon", "N.C.Hills", "Nalbari", "Nowgaon", "Sibsagar", "Sonitpur", "Tinsukia", "Udalguri"],
    "Bihar": ["Araria", "Arwal", "Aurangabad", "Banka", "Begusarai", "Bhagalpur", "Bhojpur", "Buxar", "Chapra(Saran)", "Darbhanga", "East Champaran", "Gaya", "Gopalganj", "Jahanabad", "Jamui", "Kaimur (Bhabhua)", "Katihar", "Khagaria", "Kishanganj", "Lakhisarai", "Madhepura", "Madhubani", "Munger", "Muzaffarpur", "Nalanda", "Nawada", "Patna", "Purnia", "Rohtas", "Saharsa", "Samastipur", "Sheikhpura", "Sheohar", "Sitamarhi", "Siwan", "Supaul", "Vaishali", "West Champaran"],
    "Chhattisgarh": ["Balod", "Balodabazar", "Balrampur", "Bastar", "Bemetra", "Bijapur", "Bilaspur", "Dantewada", "Dhamtari", "Durg", "Gariaband", "Gaurella Pendra Marwahi", "Jangir-Champa", "Jashpur", "Kanker", "Kawardha", "Kondagaon", "Korba", "Koria", "Mahasamund", "Mungeli", "Narayanpur", "Raigarh", "Raipur", "Rajnandgaon", "Sukma", "Surajpur", "Surguja"],
    "Goa": ["North Goa", "South Goa"],
    "Gujarat": ["Ahmedabad", "Amreli", "Anand", "Arvalli", "Banaskantha", "Bharuch", "Bhavnagar", "Botad", "Chhotaudepur", "Dahod", "Dangs", "Devbhumi Dwarka", "Gandhinagar", "Gir Somnath", "Jamnagar", "Junagadh", "Kheda", "Kutch", "Mahisagar", "Mehsana", "Morbi", "Narmada", "Navsari", "Panchmahals", "Patan", "Porbandar", "Rajkot", "Sabarkantha", "Surat", "Surendranagar", "Tapi", "Vadodara", "Valsad"],
    "Haryana": ["Ambala", "Bhiwani", "Charkhi Dadri", "Faridabad", "Fatehabad", "Gurgaon", "Hisar", "Jhajjar", "Jind", "Kaithal", "Karnal", "Kurukshetra", "Mewat", "Mohindergarh", "Palwal", "Panchkula", "Panipat", "Rewari", "Rohtak", "Sirsa", "Sonepat", "Yamuna Nagar"],
    "Himachal Pradesh": ["Bilaspur", "Chamba", "Hamirpur", "Kangra", "Kinnaur", "Kullu", "Lahul And Spiti", "Mandi", "Shimla", "Sirmaur", "Solan", "Una"],
    "Jammu And Kashmir": ["Anantnag", "Bandipora", "Baramula", "Budgam", "Doda", "Ganderbal", "Jammu", "Kathua", "Kishtwar", "Kulgam", "Kupwara", "Poonch", "Pulwama", "Rajouri", "Ramban", "Reasi", "Samba", "Shopian", "Srinagar", "Udhampur"],
    "Jharkhand": ["Bokaro", "Chatra", "Deoghar", "Dhanbad", "Dumka", "Garhwa", "Giridih", "Godda", "Gumla", "Hazaribagh", "Jamtara", "Khunti", "Koderma", "Latehar", "Lohardaga", "Pakur", "Palamu", "Pashchimi Singhbhum", "Purbi Singhbhum", "Ramgarh", "Ranchi", "Sahibganj", "Saraikela Kharsawan", "Simdega"],
    "Karnataka": ["Bagalkot", "Bangalore R", "Bangalore U", "Belgaum", "Bellary", "Bidar", "Bijapur", "Chamarajanagar", "Chickballapur", "Chickmagalur", "Chitradurga", "Dakshina Kannada", "Davanagere", "Dharwad", "Gadag", "Gulbarga", "Hassan", "Haveri", "Kodagu", "Kolar", "Koppal", "Mandya", "Mysore", "Raichur", "Ramnagar", "Shimoga", "Tumkur", "Udupi", "Uttara Kannada", "Yadgir"],
    "Kerala": ["Alappuzha", "Ernakulam", "Idukki", "Kannur", "Kasaragod", "Kollam", "Kottayam", "Kozhikode", "Malappuram", "Palakkad", "Pathanamthitta", "Thiruvananthapuram", "Thrissur", "Wayanad"],
    "Ladakh": ["Kargil", "Leh"],
    "Madhya Pradesh": ["Agar", "Alirajpur", "Anuppur", "Ashok Nagar", "Balaghat", "Barwani", "Betul", "Bhind", "Bhopal", "Burhanpur", "Chhatarpur", "Chhindwara", "Damoh", "Datia", "Dewas", "Dhar", "Dindori", "Guna", "Gwalior", "Harda", "Hoshangabad", "Indore", "Jabalpur", "Jhabua", "Katni", "Khandwa", "Khargone", "Mandla", "Mandsour", "Morena", "Narsinghpur", "Neemuch", "Panna", "Raisen", "Rajgarh", "Ratlam", "Rewa", "Sagar", "Satna", "Sehore", "Seoni", "Shahdol", "Shajapur", "Sheopur", "Shivpuri", "Sidhi", "Singrauli", "Tikamgarh", "Ujjain", "Umaria", "Vidisha"],
    "Maharashtra": ["Ahmednagar", "Akola", "Amrawati", "Aurangabad", "Beed", "Bhandara", "Buldhana", "Chandrapur", "Dhule", "Gadchiroli", "Gondia", "Hingoli", "Jalgaon", "Jalna", "Kolhapur", "Latur", "Nagpur", "Nanded", "Nandurbar", "Nashik", "Osmanabad", "Palghar", "Parbhani", "Pune", "Raigad", "Ratnagiri", "Sangali", "Satara", "Sindhudurg", "Solapur", "Thane", "Wardha", "Washim", "Yavatmal"],
    "Manipur": ["Bishnupur", "Chandel", "Churachandpur", "Imphal East", "Imphal West", "Senapati", "Tamenglong", "Thoubal", "Ukhrul"],
    "Meghalaya": ["East Garo Hills", "East Khasi Hills", "Jaintia", "Ribhoi", "South Garo Hills", "West Garo Hills", "West Khasi Hills"],
    "Mizoram": ["Aizawl", "Champhai", "Kolasib", "Lawngtlai", "Lunglei", "Mamit", "Saiha", "Serchhip"],
    "Nagaland": ["Dimapur", "Kiphire", "Kohima", "Longleng", "Mokokchung", "Mon", "Peren", "Phek", "Tuensang", "Wokha", "Zunheboto"],
    "Odisha": ["Angul", "Balangir", "Balasore", "Bargarh", "Bhadrak", "Boudh", "Cuttack", "Deogarh", "Dhenkanal", "Gajapati", "Ganjam", "Jagatsinghpur", "Jajpur", "Jharsuguda", "Kalahandi", "Kandhamal", "Kendrapara", "Keonjhar", "Khurda", "Koraput", "Malkangiri", "Mayurbhanj", "Nawarangpur", "Nayagarh", "Nuapara", "Puri", "Rayagada", "Sambalpur", "Sonepur", "Sundargarh"],
    "Puducherry": ["Karaikal", "Puducherry"],
    "Punjab": ["Amritsar", "Barnala", "Bathinda", "Faridkot", "Fatehgarh Sahib", "Fazilka", "Firozpur", "Gurdaspur", "Hoshiarpur", "Jalandhar", "Kapurthala", "Ludhiana", "Mansa", "Moga", "Mohali", "Mukatsar", "Nawashahar", "Pathankot", "Patiala", "Ropar", "Sangrur", "Tarn Taran"],
    "Rajasthan": ["Ajmer", "Alwar", "Anoopgarh", "Balotra", "Banswara", "Baran", "Barmer", "Beawar", "Bharatpur", "Bhilwara", "Bikaner", "Bundi", "Chittaurgarh", "Churu", "Dausa", "Deeg", "Dholpur", "Didwana Kuchaman", "Dudu", "Dungarpur", "Gangapurcity", "Hanumangarh", "Jaipur Gramin", "Jaisalmer", "Jalor", "Jhalawar", "Jhunjhunun", "Jodhpur Gramin", "Karauli", "Kekri", "Khairthal Tijara", "Kota", "Kotputli Behror", "Nagaur", "Neem Ka Thana", "Pali", "Phalodi", "Pratapgarh", "Rajsamand", "Salumbar", "Sanchor", "Sawaimadhopur", "Shahpura", "Sikar", "Sirohi", "Sri Ganganagar", "Tonk", "Udaipur"],
    "Sikkim": ["East", "North", "Pakyong", "Soreng", "South", "West Sikkim"],
    "Tamil Nadu": ["Ariyalur", "Chengalpattu", "Coimbatore", "Cuddalore", "Dharmapuri", "Dindigul", "Erode", "Kallakurichi", "Kanchipuram", "Kanniyakumari", "Karur", "Krishnagiri", "Madurai", "Mayiladuthurai", "Nagapattinam", "Namakkal", "Perambalur", "Pudukkottai", "Ramanathapuram", "Ranipet", "Salem", "Sivagangai", "Tenkasi", "Thanjavur", "The Nilgiris", "Theni", "Tiruchirappalli", "Tirunelveli", "Tirupathur", "Tiruppur", "Tiruvallur", "Tiruvannamalai", "Tiruvarur", "Tuticorin", "Vellore", "Villupuram", "Virudhunagar"],
    "Telangana": ["Adilabad", "Bhadradri Kothagudem", "Jagitial", "Jangoan", "Jayashankar Bhoopalapally", "Jogulamba Gadwal", "Kamareddy", "Karimnagar", "Khammam", "Komrambheem Asifabad", "Mahaboobnagar", "Mahabubabad", "Mancherial", "Medak", "Medchal Malkajgiri", "Mulugu", "Nagarkurnool", "Nalgonda", "Narayanpet", "Nirmal", "Nizamabad", "Peddapalli", "Rajanna Sircilla", "Ranga Reddy", "Sangareddy", "Siddipet", "Suryapet", "Vikarabad", "Wanaparthy", "Warangal", "Warangal Urban", "Yadadri Bhongiri"],
    "Tripura": ["Dhalai", "Gomati", "Khowai", "North Tripura", "Sepahijala", "South Tripura", "Unakoti", "West Tripura"],
    "Uttar Pradesh": ["Agra", "Aligarh", "Ambedkarnagar", "Amethi", "Auraiya", "Ayodhya", "Azamgarh", "Badaun", "Baghpat", "Bahraich", "Ballia", "Balrampur", "Banda", "Barabanki", "Bareilly", "Basti", "Bijnor", "Bulandshahr", "Chandauli", "Chitrakoot", "Deoria", "Etah", "Etawah", "Farrukhabad", "Fatehpur", "Firozabad", "G.B. Nagar", "Ghaziabad", "Ghazipur", "Gonda", "Gorakhpur", "Hamirpur", "Hapur", "Hardoi", "Hathras", "J.B.F.Nagar", "Jalaun", "Jaunpur", "Jhansi", "Kannauj", "Kanpur Dehat", "Kanpur Nagar", "Kasganj", "Kaushambi", "Kushinagar", "Lakhimpur-Kherii", "Lalitpur", "Lucknow", "Maharajganj", "Mahoba", "Mainpuri", "Mathura", "Mau", "Meerut", "Mirzapur", "Moradabad", "Muzaffarnagar", "Pilibhit", "Pratapgarh", "Prayagraj", "Rae Bareli", "Rampur", "S.K. Nagar", "S.R. Nagar(Bhadohi)", "Saharanpur", "Sambhal", "Shahjahanpur", "Shamli", "Shrawasti", "Siddharathnagar", "Sitapur", "Sonebhadra", "Sultanpur", "Unnao", "Varanasi"],
    "Uttarakhand": ["Almora", "Bageshwar", "Chamoli", "Champawat", "Dehradun", "Haridwar", "Nainital", "Pauri", "Pithoragarh", "Rudraprayag", "Tehri", "Udham Singh Nagar", "Uttarkashi"],
    "West Bengal": ["Alipurduar", "Bankura", "Birbhum", "Cooch-Behar", "Dakshin Dinajpur", "Darjeeling", "Hooghly", "Howrah", "Jalpaiguri", "Jhargram", "Kalimpong", "Maldah", "Murshidabad", "Nadia", "North 24 Parganas", "Paschim Burdwan", "Paschim Medinipur", "Purba Burdwan", "Purba Medinipur", "Purulia", "Siliguri M.P.", "South 24-Parganas", "Uttardinajpur"]
}


# ----------------- IBM Cloud WML Config ------------------
API_KEY = "0QfzNqqBLe5xJFxi6admmnnkPDL9TS9Z5H3KBi8jroGl" # ⚠️ IMPORTANT: Replace with your actual API key
DEPLOYMENT_URL = "https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/pmsgy/predictions?version=2021-05-01"

# ----------------- Streamlit UI ------------------
st.set_page_config(
    page_title="PMGSY Project Classifier",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Main app background with a light, clean gradient */
    .stApp {
        background: #ece9e6;  /* fallback for old browsers */
        background: -webkit-linear-gradient(to right, #ffffff, #ece9e6, #ffffff);  /* Chrome 10-25, Safari 5.1-6 */
        background: linear-gradient(to right, #ffffff, #ece9e6, #ffffff); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
        background-attachment: fixed;
        background-size: cover;
        color: #333333; /* Dark gray text for contrast */
    }

    /* Input widgets styling */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div {
        background-color: #90EE90; /* Light gray background */
        color: #333333;
        border-radius: 5px;
        border: 1px solid #cccccc;
        padding: 8px 12px;
    }
    .stSelectbox>div>div {
        padding: 0 12px; /* Adjust padding for selectbox */
    }
    
    /* Custom styling for the progress bar */
    .stProgress > div > div > div > div {
        background-color: #4CAF50; /* Green progress bar */
    }

    /* Button styling */
    .stButton>button {
        color: #ffffff;
        background-color: #007bff; /* Blue button */
        border-radius: 5px;
        border: 1px solid #007bff;
        font-weight: normal;
        transition: all 0.2s ease-in-out;
        padding: 10px 20px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    }
    .stButton>button:hover {
        background-color: #0056b3;
        border-color: #0056b3;
        transform: translateY(-2px);
        box-shadow: 2px 4px 8px rgba(0,0,0,0.3);
    }
    
    /* Metric styling for the result */
    [data-testid="stMetricValue"] {
        font-size: 2.5em;
        color: #007bff; /* Blue for metric value */
        font-weight: bold;
    }
    [data-testid="stMetricLabel"] {
        font-size: 1.2em;
        color: #666666; /* Medium gray for label */
    }

    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #0056b3; /* Darker blue for headers */
    }

    /* Warnings */
    .stAlert {
        background-color: #fff3cd;
        color: #856404;
        border-color: #ffeeba;
    }

    /* Success messages */
    .stSuccess {
        background-color: #d4edda;
        color: #155724;
        border-color: #c3e6cb;
    }

</style>
""", unsafe_allow_html=True)

st.title("PMGSY (pradhan Mantri gramin Sarak yojna) Project Classifier")
st.markdown("A Streamlit application to classify rural infrastructure projects.")

# Use a sidebar for inputs
st.sidebar.header("Project Details")

# Input fields for project location
state = st.sidebar.selectbox(
    "Select State",
    options=list(state_district_map.keys()),
    index=0
)

district_options = state_district_map.get(state, [])
district = st.sidebar.selectbox(
    "Select District",
    options=district_options,
    index=0 if district_options else None
)

st.sidebar.markdown("### Project Metrics")

# Input fields for project metrics
no_road_san = st.sidebar.number_input("Number of Road Works Sanctioned", min_value=0, value=0)
length_road_san = st.sidebar.number_input("Length of Road Work Sanctioned (in km)", min_value=0.0, value=0.0)
no_bridge_san = st.sidebar.number_input("Number of Bridges Sanctioned", min_value=0, value=0)
cost_work_san = st.sidebar.number_input("Cost of Works Sanctioned (in Lakhs)", min_value=0.0, value=0.0)

no_road_comp = st.sidebar.number_input("Number of Road Works Completed", min_value=0, value=0)
length_road_comp = st.sidebar.number_input("Length of Road Work Completed (in km)", min_value=0.0, value=0.0)
no_bridge_comp = st.sidebar.number_input("Number of Bridges Completed", min_value=0, value=0)
exp_occurred = st.sidebar.number_input("Expenditure Occurred (in Lakhs)", min_value=0.0, value=0.0)

no_road_bal = st.sidebar.number_input("Number of Road Works Balance", min_value=0, value=0)
length_road_bal = st.sidebar.number_input("Length of Road Work Balance (in km)", min_value=0.0, value=0.0)
no_bridge_bal = st.sidebar.number_input("Number of Bridges Balance", min_value=0, value=0)

if st.sidebar.button("Classify Project"):
    if not state or not district:
        st.sidebar.warning("Please select both State and District.")
    else:
        with st.spinner('Classifying...'):
            # Step 1: Get IBM Cloud IAM Token
            try:
                iam_response = requests.post(
                    "https://iam.cloud.ibm.com/identity/token",
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    data=f"apikey={API_KEY}&grant_type=urn:ibm:params:oauth:grant-type:apikey"
                )
                iam_response.raise_for_status()
                access_token = iam_response.json()["access_token"]
            except Exception as e:
                st.error(f"Failed to get IBM Cloud IAM Token. Error: {e}")
                st.stop()

            # Step 2: Prepare payload for WML prediction
            payload = {
                "input_data": [{
                    "fields": [
                        "STATE_NAME", "DISTRICT_NAME", "NO_OF_ROAD_WORK_SANCTIONED",
                        "LENGTH_OF_ROAD_WORK_SANCTIONED", "NO_OF_BRIDGES_SANCTIONED",
                        "COST_OF_WORKS_SANCTIONED", "NO_OF_ROAD_WORKS_COMPLETED",
                        "LENGTH_OF_ROAD_WORK_COMPLETED", "NO_OF_BRIDGES_COMPLETED",
                        "EXPENDITURE_OCCURED", "NO_OF_ROAD_WORKS_BALANCE",
                        "LENGTH_OF_ROAD_WORK_BALANCE", "NO_OF_BRIDGES_BALANCE"
                    ],
                    "values": [[
                        state, district, no_road_san, length_road_san,
                        no_bridge_san, cost_work_san, no_road_comp, length_road_comp,
                        no_bridge_comp, exp_occurred, no_road_bal, length_road_bal,
                        no_bridge_bal
                    ]]
                }]
            }

            # Step 3: Make prediction
            try:
                response = requests.post(
                    DEPLOYMENT_URL,
                    headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
                    data=json.dumps(payload)
                )
                response.raise_for_status()
                result = response.json()
                
                pred_label = result['predictions'][0]['values'][0][0]
                pred_probs = result['predictions'][0]['values'][0][1]
                confidence = max(pred_probs) # Get the highest probability
                
                st.success("✅ Classification Complete!")
                st.markdown("## Prediction Result:")
                
                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    st.metric(label="Project Class", value=str(pred_label))
                with res_col2:
                    st.metric(label="Confidence", value=f"{confidence*100:.2f}%")
                
                st.progress(confidence)


            except Exception as e:
                st.error(f"Prediction Failed. Error: {e}")
                st.stop()

st.markdown("""
<hr>
<div style="text-align:center; padding-top: 20px;">
    <p style="font-size: 1.1em; color: #333333;"> <!-- Changed text color to match new theme -->
        Built with dedication and data by <strong>Himanshu kumar</strong> 🚀
    </p>
    <p style="font-size: 0.9em; color: #555555;">
        <h6>A MCA Postgraduate @ Dr B C Roy Engineering college ,Durgapur.</h6>
    </p>
    <p style="font-size: 1.0em; margin-top: 15px;">
        <a href="www.linkedin.com/in/himanshu-kumar-4214b722b/" target="_blank" style="text-decoration: none; color: #0077B5; margin: 0 10px;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/LinkedIn_logo_initials.png/480px-LinkedIn_logo_initials.png" width="20" height="20" style="vertical-align: middle;"> LinkedIn
        </a> |
        <a href="https://www.instagram.com/himanshukashyap_20?igsh=MW0zYjNwNnBwcWN6OQ==/" target="_blank" style="text-decoration: none; color: #C13584; margin: 0 10px;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Instagram_logo_2016.svg/768px-Instagram_logo_2016.svg.png" width="20" height="20" style="vertical-align: middle;"> Instagram
        </a> |
       <a href="https://github.com/kashypHi" target="_blank" style="text-decoration: none; color: #007bff; margin: 0 10px;">
            <img src="https://icones.pro/wp-content/uploads/2021/06/icone-github-orange.png" width="20" height="20" style="vertical-align: middle;"> View in GitHub
        </a>
            |
    </p>
</div>
""", unsafe_allow_html=True)
