from . import LEVEL


def get_today() -> dict:
    return {
        "today": {
            "level": LEVEL[0],
            "temp": LEVEL[0],
            "rain": LEVEL[1],
            "air": LEVEL[0],
            "job": "진드기 물림 사고",
        },
    }


def get_details() -> dict:
    return {
        "tips": [
            "진드기 물림 사고 예방을 위해 긴팔, 긴바지를 착용하고, 외출 후에는 반드시 샤워를 하세요.",
            "야외 활동 후에는 옷을 털고, 진드기가 붙어 있는지 확인하세요.",
            "진드기 물림 사고가 발생하면 즉시 병원에 방문하여 치료를 받으세요.",
            "온열손상 예방을 위해 작업 간 온열손상키트를 휴대하고, 50분마다 10분씩 휴식을 부여하세요.",
        ],
        "jobs": [
            {
                "job": "진드기 물림",
                "level": LEVEL[2],
            },
            {
                "job": "온열 손상",
                "level": LEVEL[1],
            },
            {
                "job": "낙상",
                "level": LEVEL[0],
            },
            {
                "job": "자살",
                "level": LEVEL[0],
            },
        ],
    }


def get_forecast() -> dict:
    return {
        "forecast": [
            {
                "week": "자율적 부대운영",
                "level": LEVEL[0],
                "job": "없음",
            },
            {
                "week": "훈련 준비",
                "level": LEVEL[1],
                "job": "기동 간 안전사고",
            },
            {
                "week": "포대 전술훈련",
                "level": LEVEL[2],
                "job": "기동 간 안전사고",
            },
            {
                "week": "훈련 후 정비",
                "level": LEVEL[0],
                "job": "없음",
            },
        ],
    }
