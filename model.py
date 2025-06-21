course_requirements = {
    "Computer Science": {
        "utme": >= 240,
        "post_utme": >= 75,
        "olevel": {
            "required": ["English", "Maths", "Physics"],  # Must-have subjects
            "optional": {
                "choices": ["Biology", "Chemistry", "Agric"],  # Pick any 2
                "min_passes": 2
            },
            "max_grade": 6  # A1–C6 are acceptable
        }
    },
    "Microbiology": {
        "utme": >= 230,
        "post_utme": >= 70,
        "olevel": {
            "required": ["English", "Maths", "Biology", "Agric"],
            "optional": {
                "choices": ["Physics", "Chemistry"],
                "min_passes": 1
            },
            "max_grade": 6
        }
    }
    "Biochemistry": {
        "utme": >=225,
        "post_utme": >= 70,
        "olevel": {
            "required": ["English", "Maths", "Chemistry", "Biology"],
            "optional": {
                "choices": ["Physics", "Agric"],
                "min_passes": 1
            },
            "max_grade": 6
        }
    }
    "Physics": {
        "utme": >=220,
        "post_utme": >= 68,
        "olevel": {
            "required": ["English", "Maths", "Physics", "Chemistry"],
            "optional": {
                "choices": ["Biology", "Agric"],
                "min_passes": 1
            },
            "max_grade": 6
        }
    }
    "Applied Physics": {
        "utme": >= 215,
        "post_utme": >= 66,
        "olevel": {
            "required": ["English", "Maths", "Physics", "Chemistry"],
            "optional": {
                "choices": ["Biology", "Agric"],
                "min_passes": 1
            },
            "max_grade": 6
        }
    }
    "Industrial Chemistry": {
        "utme": >= 210,
        "post_utme": >= 65,
        "olevel": {
            "required": ["English", "Maths", "Physics", "Chemistry"],
            "optional": {
                "choices": ["Agric", "Biology"],
                "min_passes": 1
            },
            "max_grade": 6
        }
    }
    "Mathematics and Statistics": {
        "utme": >= 205,
        "post_utme": >= 65,
        "olevel": {
            "required": ["English", "Maths", "Physics", "Chemistry"],
            "optional": {
                "choices": ["Agric", "Biology"],
                "min_passes": 1
            },
            "max_grade": 6
        }
    }
    "Animal and environmental biology": {
        "utme": >= 203,
        "post_utme": >= 60,
        "olevel": {
            "required": ["English", "Maths", "Agric", "Biology"],
            "optional": {
                "choices": ["Physics", "Chemistry" ],
                "min_passes": 1
            },
            "max_grade": 6
        }
    }
    " Plant Science and Biotechnology": {
        "utme": >= 200,
        "post_utme": >= 60,
        "olevel": {
            "required": ["English", "Maths", "Agric", "Biology"],
            "optional": {
                "choices": ["Physics", "Chemistry" ],
                "min_passes": 1
            },
            "max_grade": 6
        }
    }
}
