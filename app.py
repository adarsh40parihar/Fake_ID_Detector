import pickle
import streamlit as st
import instaloader
import json
import csv
# import os
import sys
import shutil
import numpy as np
import time
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from scipy.stats import randint
from instaloader.exceptions import LoginRequiredException

pickle_in = open("classifier.pkl", "rb")
model = pickle.load(pickle_in)

classes = ["", 0, 1]

def myuser1(user):
    L = instaloader.Instaloader()
    username = 'sih_2023_14'
    password = 'qwerty123456'

    try:

        profile = instaloader.Profile.from_username(L.context, user)

    except LoginRequiredException:
        try:
            L.load_session_from_file(name)
            profile = instaloader.Profile.from_username(L.context, user)

        except instaloader.exceptions.QueryReturnedBadRequestException as e:
            pass

        L.save_session_to_file()

    except Exception as e:

        pass

def scrap(user):
    usrname = user
    ig = instaloader.Instaloader()

    profile = instaloader.Profile.from_username(ig.context, usrname)

    with open(r"./given_test.txt", 'w') as f:
        sys.stdout = f
        instaloader.Instaloader().download_profile(usrname, profile_pic_only=True)

    sys.stdout = sys.stdout

    input_file_name = r"./given_test.txt"
    str_check = ""
    with open(input_file_name, "r") as input_file:
        line = input_file.readline()
        str_check = input_file.read()

    y = len(usrname) + 1
    jh = "2018-11-21_19-35-46_UTC_profile_pic.jpg " + "\n"
    check = str_check[y:]
    profile_pic = 0

    if check == jh:
        profile_pic = 0
    else:
        profile_pic = 1

    input_file.close()
    shutil.rmtree(usrname)

    x = 0
    if profile.is_private:
        x = 1
    else:
        x = 0

    digit_count = sum(1 for char in profile.username if char.isdigit())

    data = [{
        "FollowerCount": int(profile.followers),
        "FollowingCount": int(profile.followees),
        "BioLength": len(profile.biography),
        "Posts": profile.mediacount,
        "HasProfilePic": profile_pic,
        "IsPrivate": x,
        "usernameDigitCount": digit_count / len(profile.username)
    }]

    file_path = r"./given_user_json.json"
    with open(file_path, 'w') as json_file:

        json.dump(data, json_file)

    with open(r"./given_user_json.json") as json_file:
        jsondata = json.load(json_file)

    data_file = open(r"./given_user_csv.csv", 'w', newline='')
    csv_writer = csv.writer(data_file)

    count = 0
    for data in jsondata:
        if count == 0:
            header = data.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow(data.values())

    return data


def prediction(ans):
    prediction = model.predict(ans)
    return prediction


def main():
    st.title("Fake Instagram Detector")

    user = st.text_input("Enter the username")
    myuser1(user)

    if st.button("Detect"):
        data = scrap(user)

        ans = []
        for keys in data:
            ans.append(data[keys])

        ans = np.array(ans)
        ans = ans.reshape(1, -1)
        fake = prediction(ans)
        time.sleep(1)

        st.markdown(
            '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">',
            unsafe_allow_html=True)

        if fake == 0:
            # st.success('bhai tera to genuine hai')
            # st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">', unsafe_allow_html=True)
            htmlstr = """
                    <style>
                    .green-tick {
                        color: #2ecc71; 
                        font-size: 24px; 
                        margin-right: 8px; 
                        border-radius: 7xp;
                        padding-left: 12px;
                        padding-bottom: 13px;
                        padding-top:13px;
                    }
                    </style>
                    """
            st.markdown(htmlstr, unsafe_allow_html=True)
            st.markdown('<i class="green-tick fas fa-check-circle"></i> Bhai tera genuine hai', unsafe_allow_html=True)
        else:
            htmlstr = """
                    <style>
                    .icon {
                        color: #ff0000; 
                        font-size: 24px; 
                        margin-right: 8px; 
                        border-radius: 7xp;
                        padding-left: 12px;
                        padding-bottom: 13px;
                        padding-top:13px;
                    }
                    </style>
                    """
            st.markdown(htmlstr, unsafe_allow_html=True)
            st.markdown('<i class="icon fas fa-times"></i> Tu to gyo', unsafe_allow_html=True)


if __name__ == '__main__':
    main()
