import streamlit as st
import pandas as pd

st.title("Electricity Bill Calculator",width="stretch")

#Initialize Variables
noOfUnits=0

#Create columns to control layout
col1,col2,col3=st.columns([3,1,1]) #✅🧠Column මුළු එකතුව මත පදනම්ව අනුපාත ස්වයංක්‍රීයව සාමාන්‍යකරණය වේ. 60%,20%,20%

with col1:
    #radio button to choose input type
    status=st.radio("Select an option:",['Readings','No of Units'],horizontal=True)

    #input logic
    if status == "Readings":                                                                             #✅🧠 format="%d" -- පූර්ණ සංඛ්‍යාවක් ලෙස පමණක් ආකෘතිකරණය කරන්න (එනම්, දශම ලක්ෂ්‍ය පෙන්වා නැත).
        preReading =st.number_input("Enter last month reading",key="pre",min_value=0,step=1,format="%d") #✅🧠 step=1 -- ඉහළ/පහළ ඊතල ක්ලික් කිරීමෙන් සංඛ්‍යාව 1 කින් වැඩි වේ/අඩු වේ.
        curReading=st.number_input("Enter this month reading",key="cur",min_value=0,step=1,format="%d")  #✅🧠 min_value=0 -- පරිශීලකයින් සෘණ අගයන් ඇතුළත් කිරීමෙන් වළක්වයි. මීටර කියවීම් සෘණ විය නොහැක.
                                                                                                         # ⚠️ වැදගත්: st.number_input සෑම විටම අංකයක් ආපසු ලබා දෙයි, කිසිවක් ඇතුළත් නොකළහොත් defaulting 0 වේ.
        if preReading and curReading:
            preReading=int(preReading)
            curReading =int(curReading)

            if curReading > preReading:
                noOfUnits=curReading - preReading
            else:
                st.warning("Current reading must be greater than or equal to previous reading.")

    elif status == "No of Units":
        noOfUnits=st.number_input("Enter number of units used",key="units",min_value=0,step=1,format="%d")


    #calculate button
    if st.button("Calculate") and noOfUnits > 0:
        try:
            row=[] #✅🧠බිල්පත් OUTPUT වගුව සඳහා එක් එක් පේළියේ දත්ත ගබඩා කිරීමට  එය භාවිතා කරනු ඇත.

            #fixed charge
            fixed_charge=round(350.00,2)
            unit_cost=0.00
            units_remaining=noOfUnits

            #for first 20 units
            if units_remaining >0:
                units=min(20,units_remaining)
                cost=round(5.00*units,2) #✅🧠 2 යොදා ඇත්තේ ආසන්න දශමස්ථාන දෙකකට පිලිතුර ගැනීම සඳහාය.
                row.append(["First 20 units",units,5.00,cost])
                unit_cost += cost
                units_remaining -= units

            #for second 50 units
            if units_remaining >0:
                units=min(50,units_remaining)
                cost=round(7.00*units,2)
                row.append(["Second 50 units",units,7.00,cost])
                unit_cost += cost
                units_remaining -= units

            #remaining units
            if units_remaining >0:
                cost=round(units_remaining * 10.00,2)
                row.append(["Remaining units",units_remaining,10.00,cost])
                unit_cost += cost

            total_cost=fixed_charge + unit_cost

            #add fixed charge
            row.append(["Fixed Charge", "--","--",fixed_charge])

            total_cost=round(unit_cost + fixed_charge,2)
            row.append(["Total Charge","--","--",total_cost])

            #show result
            st.info(f"Total Charge: Rs.{total_cost:.2f}")

            #convert to dataframe and show table
            df=pd.DataFrame(row,columns=["Description","Units(KWh)","Rate (Rs.)","Cost (Rs.)"]) #✅🧠DataFrame එකක් යනු Excel වගුවක් වැනිය — ලේබල් කරන ලද ශීර්ෂ සහිත පේළි සහ තීරු.එය Python හි වගු දත්ත සමඟ වැඩ කිරීම සඳහා භාවිතා කරන pandas පුස්තකාලයේ කොටසකි.

            #format the rate and cost columns
            df["Rate (Rs.)"] = df["Rate (Rs.)"].apply(lambda x: f"{x:.2f}" if isinstance(x,(int,float))else x)
            df["Cost (Rs.)"] = df["Cost (Rs.)"].apply(lambda x: f"{x:.2f}" if isinstance(x,(int,float))else x)
            st.table(df)

            with col2:
                if st.button("Reset"):
                    st.session_state["pre"] = 0
                    st.session_state["cur"] = 0


        except Exception as e:
            st.error(f"Error calculating bill:{e}")
