# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be:", name_on_order)

ctx = st.connection("snowflake")
session = ctx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ing_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections = 5
)

if ing_list:
    ing_string = ''
    for fruit in ing_list:
        ing_string += fruit + ' '

    # st.write(ing_string)

    my_insert = """insert into smoothies.public.orders(ingredients, name_on_order)
    values ('""" + ing_string + "', '" + name_on_order + "')"

    st.write(my_insert)
    # st.stop()
    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert).collect()
        st.success("Your Smoothie is ordered!", icon="✅")

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)
