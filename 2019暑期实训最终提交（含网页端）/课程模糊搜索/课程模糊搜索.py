class CoursesSearch(APIView):
    """
    ¿Î³ÌÄ£ºýËÑË÷
    """
    permission_classes = (SignaturePermission, )
    serializer_class = CoursesSearchSerializer

    def get(self, request):
        serializer = self.serializer_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        name = serializer.validated_data['name']
        query = Course.manager.all().filter(name__icontains=name).values()
        courses = []
        for course in query:
            if course['name'] not in courses:
                courses.append(course['name'])
        return Response(courses)