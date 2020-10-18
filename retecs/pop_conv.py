"""
COPYRIGHT © BSH HOME APPLIANCES GROUP  2020

ALLE RECHTE VORBEHALTEN. ALL RIGHTS RESERVED.

The reproduction, transmission or use of this document or its contents is not permitted without express
written authority. Offenders will be liable for damages. All rights, including rights created by  patent
grant or registration of a utility model or design, are reserved.
"""
import pickle
import json
import os
from artifactory import ArtifactoryPath
import requests.packages.urllib3 as urllib3


class PopConv:

    def __init__(self, pickle_path):
        self.pickle_path = pickle_path

    def __load(self):
        return pickle.load(open(self.pickle_path, 'rb'))

    def __convert(self, data):
        population = data.population
        converted = list(map(lambda x: x.convert_python_to_json(), population))
        json_path = self.pickle_path.split(".")[0] + ".json"
        with open(json_path, "w") as file:
            json.dump(converted, file, sort_keys=True, indent=4)

    def load_and_convert(self):
        self.__convert(self.__load())

    @staticmethod
    def convert_everything():
        root = r"C:\Users\RosenbauerL\PycharmProjects\ci_xcs\retecs\OLD_AGENTS" + os.sep + "rq_xcsf_er_gsdtsr_timerank_"
        for i in range(0, 30):
            curr_path = root + str(i) + "_agent.p"
            PopConv(curr_path).load_and_convert()


class ArtifactoryPusher:

    def __init__(self, json_path, usr="rosenbauerl", cred="AKCp5e2gQ1gKgUmPNh2RTCf6X1qW7ePmC3h3i4svEC32s6S9NaDuRCYB2Ugr3WEhjkrz2VvNP", root=r"https://production.artifactory.bshg.com/artifactory/mason_testing_results/OrganicTester/KnowledgeBase/"):
        self.json_path = json_path
        self.user = usr
        self.credentials = cred
        self.root = root
        # Disable ssl warnings inside the company
        urllib3.disable_warnings()

    def deploy_file(self):
        directory = self.json_path.split(os.sep)[-1]
        artifactory_path = self.root + directory
        if artifactory_path[-1] != "/":
            artifactory_path += "/"
        # connnect to artifactory & upload
        artifactory_ref = ArtifactoryPath(artifactory_path, auth=(self.user, self.credentials), verify=False)
        artifactory_ref.deploy_file(self.json_path)

    @staticmethod
    def upload_everything():
        root = r"C:\Users\RosenbauerL\PycharmProjects\ci_xcs\retecs\OLD_AGENTS" + os.sep + "rq_xcsf_er_gsdtsr_timerank_"
        for i in range(0, 30):
            curr_path = root + str(i) + "_agent.json"
            ArtifactoryPusher(curr_path).deploy_file()
