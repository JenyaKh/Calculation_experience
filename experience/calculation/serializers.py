from rest_framework import serializers

from calculation.models import Candidate, Experience
from datetime import datetime


class ExperienceSerializer(serializers.ModelSerializer):

    start = serializers.CharField()
    end = serializers.CharField()

    class Meta:
        model = Experience
        fields = ['start', 'end']


class CandidateSerializer(serializers.ModelSerializer):

    workExperience = ExperienceSerializer(many=True, source='experiences')
    id = serializers.IntegerField(required=False)
    totalExperience = serializers.IntegerField(source='total_experience', required=False)
    name = serializers.CharField()

    class Meta:
        model = Candidate
        fields = ['id', 'name', 'totalExperience', 'workExperience']

    def create(self, validated_data):
        experiences = validated_data.pop('experiences')
        candidate = Candidate.objects.create(**validated_data)
        for experience in experiences:
            Experience.objects.create(candidate=candidate, **experience)

        date_format = "%b %Y"
        all_experience = []

        # get the entire experience of this candidate
        work_experience = candidate.experiences.all()

        # converting the start and end date of work to the datetime format
        for experience in work_experience:
            all_experience.append([datetime.strptime(experience.start, date_format),
                                   datetime.strptime(experience.end, date_format)])

        # sorting work experience by start date
        all_experience.sort()

        # assign the variables the start and end date of the candidate's first job
        start_work = all_experience[0][0]
        end_work = all_experience[0][1]

        # calculate the seniority in the first place of work, including the first and last months
        total = (end_work - start_work).days//30 + 1
        print(total)
        # calculate the experience for the following jobs
        for experience in all_experience[1:]:
            start_exp = experience[0]
            end_exp = experience[1]

        # if the start date of the new job is before the end of the previous one
        # and the end date is greater than the previous one
            if start_exp < end_work:
                if end_exp > end_work:
                    total += (end_exp - end_work).days//30
                    print(total)

        # if the start date of the new job is greater than the end date of the previous one
            if start_exp > end_work:
                total += (end_exp - start_exp).days//30 + 1
                print(total)

        # if the start date of the new job is equal to the end date of the previous one
            if start_exp == end_work:
                total += (end_exp - start_exp).days//30
                print(total)

        # if the end date of the new job is greater than the end date of the previous one,
        # update the value end_work
            if end_exp > end_work:
                end_work = end_exp

        # calculate the total experience in years
        total = total//12
        # updating the total experience field in the candidate model
        candidate.total_experience = total
        candidate.save()

        return candidate
