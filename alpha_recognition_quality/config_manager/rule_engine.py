class RuleEngineV3:
    RULE_PATH = "rule_engine.rules."
    SINGLE_BORDER_RULE_PATH = RULE_PATH + "single_border_rule.{module}"
    MULTI_BORDER_RULE_PATH = RULE_PATH + "multi_border_rule.{module}"
    CROSS_MAJOR_RULE_PATH = RULE_PATH + "cross_major_rule.{module}"

    """
    "规则ID": {
        "major": "专业"
        "pack": "包名",
        "module": "文件名",
        "class_name": "规则类名",
        "checkpoint_amount": 2
    }
    """
    RULE = {
        # 建筑单图框
        "1100001": {
            "major": "architecture",
            "pack": "PL",
            "module": "rule_1100001",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1100012": {
            "major": "architecture",
            "pack": "PL",
            "module": "rule_1100012",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1100002": {
            "major": "architecture",
            "pack": "PL",
            "module": "rule_1100002",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1100003": {
            "major": "architecture",
            "pack": "PL",
            "module": "rule_1100003",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1100004": {
            "major": "architecture",
            "pack": "PL",
            "module": "rule_1100004",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1100006": {
            "major": "architecture",
            "pack": "PL",
            "module": "rule_1100006",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1100007": {
            "major": "architecture",
            "pack": "PL",
            "module": "rule_1100007",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1100008": {
            "major": "architecture",
            "pack": "PL",
            "module": "rule_1100008",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1100009": {
            "major": "architecture",
            "pack": "PL",
            "module": "rule_1100009",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1100010": {
            "major": "architecture",
            "pack": "PL",
            "module": "rule_1100010",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1100011": {
            "major": "architecture",
            "pack": "PL",
            "module": "rule_1100011",
            "class_name": "Rule",
            "checkpoint_amount": 1
        },

        "1100019": {
            "major": "architecture",
            "pack": "PL",
            "module": "rule_1100019",
            "class_name": "Rule",
            "checkpoint_amount": 1
        },

        "1100027": {
            "major": "architecture",
            "pack": "PL",
            "module": "rule_1100027",
            "class_name": "Rule",
            "checkpoint_amount": 1
        },
        "1100054": {
            "major": "architecture",
            "pack": "PL",
            "module": "rule_1100054",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1100051": {
            "major": "architecture",
            "pack": "PL",
            "module": "rule_1100051",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1100005": {
            "major": "architecture",
            "pack": "PL",
            "module": "rule_1100005",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },

        "1100028": {
            "major": "architecture",
            "pack": "PL",
            "module": "rule_1100028",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1100050": {
            "major": "architecture",
            "pack": "PL",
            "module": "rule_1100050",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },

        "1102005": {
            "major": "architecture",
            "pack": "JM",
            "module": "rule_1102005",
            "class_name": "Rule",
            "checkpoint_amount": 3,
        },
        "1102021": {
            "major": "architecture",
            "pack": "JM",
            "module": "rule_1102021",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1100034": {
            "major": "architecture",
            "pack": "PL",
            "module": "rule_1100034",
            "class_name": "Rule",
            "checkpoint_amount": 6,
        },
        "1100040": {
            "major": "architecture",
            "pack": "PL",
            "module": "rule_1100040",
            "class_name": "Rule",
            "checkpoint_amount": 3,
        },
        "1100043": {
            "major": "architecture",
            "pack": "PL",
            "module": "rule_1100043",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1100047": {
            "major": "architecture",
            "pack": "PL",
            "module": "rule_1100047",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1100053": {
            "major": "architecture",
            "pack": "PL",
            "module": "rule_1100053",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1102020": {
            "major": "architecture",
            "pack": "JM",
            "module": "rule_1102020",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1102022": {
            "major": "architecture",
            "pack": "JM",
            "module": "rule_1102022",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1102023": {
            "major": "architecture",
            "pack": "JM",
            "module": "rule_1102023",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1102024": {
            "major": "architecture",
            "pack": "JM",
            "module": "rule_1102024",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1102025": {
            "major": "architecture",
            "pack": "JM",
            "module": "rule_1102025",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1102026": {
            "major": "architecture",
            "pack": "JM",
            "module": "rule_1102026",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1100029": {
            "major": "architecture",
            "pack": "JM",
            "module": "rule_1100029",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104001": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104001",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104004": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104004",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104003": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104003",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1104025": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104025",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1104009": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104009",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104011": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104011",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104013": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104013",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104017": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104017",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104022": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104022",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1204001": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1204001",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1204003": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1204003",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104023": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104023",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104016": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104016",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104032": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104032",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104034": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104034",
            "class_name": "Rule",
            "checkpoint_amount": 3,
        },
        "1104036": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104036",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104038": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104038",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104040": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104040",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104044": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104044",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104045": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104045",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104047": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104047",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104050": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104050",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104051": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104051",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104052": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104052",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104053": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104053",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104055": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104055",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104012": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104012",
            "class_name": "Rule",
            "checkpoint_amount": 3,
        },
        "1104049": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104049",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1105001": {
            "major": "architecture",
            "pack": "BL",
            "module": "rule_1105001",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1105002": {
            "major": "architecture",
            "pack": "BL",
            "module": "rule_1105002",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1105003": {
            "major": "architecture",
            "pack": "BL",
            "module": "rule_1105003",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1105005": {
            "major": "architecture",
            "pack": "BL",
            "module": "rule_1105005",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1105004": {
            "major": "architecture",
            "pack": "BL",
            "module": "rule_1105004",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1102002": {
            "major": "architecture",
            "pack": "JM",
            "module": "rule_1102002",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1102001": {
            "major": "architecture",
            "pack": "JM",
            "module": "rule_1102001",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1102008": {
            "major": "architecture",
            "pack": "JM",
            "module": "rule_1102008",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1102010": {
            "major": "architecture",
            "pack": "JM",
            "module": "rule_1102010",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1102003": {
            "major": "architecture",
            "pack": "JM",
            "module": "rule_1102003",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1102012": {
            "major": "architecture",
            "pack": "JM",
            "module": "rule_1102012",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1102013": {
            "major": "architecture",
            "pack": "JM",
            "module": "rule_1102013",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1102014": {
            "major": "architecture",
            "pack": "JM",
            "module": "rule_1102014",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1102015": {
            "major": "architecture",
            "pack": "JM",
            "module": "rule_1102015",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1102016": {
            "major": "architecture",
            "pack": "JM",
            "module": "rule_1102016",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1104002": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104002",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104010": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104010",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104014": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104014",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104039": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104039",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1104026": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104026",
            "class_name": "Rule",
            "checkpoint_amount": 3,
        },
        "1104041": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104041",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1502018": {
            "major": "electric",
            "pack": "JM",
            "module": "rule_1502018",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        # 结构
        "1204002": {
            "major": "structure",
            "pack": "ZH",
            "module": "rule_1204002",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        # 建筑跨图框
        "1102006": {
            "major": "architecture",
            "pack": "JM",
            "module": "rule_1102006",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1102011": {
            "major": "architecture",
            "pack": "JM",
            "module": "rule_1102011",
            "class_name": "Rule",
            "checkpoint_amount": 3,
        },
        "1102009": {
            "major": "architecture",
            "pack": "JM",
            "module": "rule_1102009",
            "class_name": "Rule",
            "checkpoint_amount": 15,
        },
        "1104042": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104042",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        # 给排水
        "1300002": {
            "major": "plumbing",
            "pack": "PL",
            "module": "rule_1300002",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1300006": {
            "major": "plumbing",
            "pack": "PL",
            "module": "rule_1300006",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1300007": {
            "major": "plumbing",
            "pack": "PL",
            "module": "rule_1300007",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1300018": {
            "major": "plumbing",
            "pack": "PL",
            "module": "rule_1300018",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        '1300022': {
            "major": "plumbing",
            "pack": "PL",
            "module": "rule_1300022",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1300027": {
            "major": "plumbing",
            "pack": "PL",
            "module": "rule_1300027",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1300029": {
            "major": "plumbing",
            "pack": "PL",
            "module": "rule_1300029",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1300031": {
            "major": "plumbing",
            "pack": "PL",
            "module": "rule_1300031",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1300036": {
            "major": "plumbing",
            "pack": "PL",
            "module": "rule_1300036",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1300037": {
            "major": "plumbing",
            "pack": "PL",
            "module": "rule_1300037",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1300040": {
            "major": "plumbing",
            "pack": "PL",
            "module": "rule_1300040",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1300043": {
            "major": "plumbing",
            "pack": "PL",
            "module": "rule_1300043",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1300046": {
            "major": "plumbing",
            "pack": "PL",
            "module": "rule_1300046",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1300049": {
            "major": "plumbing",
            "pack": "PL",
            "module": "rule_1300049",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1302001": {
            "major": "plumbing",
            "pack": "JM",
            "module": "rule_1302001",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1302002": {
            "major": "plumbing",
            "pack": "JM",
            "module": "rule_1302002",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1302003": {
            "major": "plumbing",
            "pack": "JM",
            "module": "rule_1302003",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1302004": {
            "major": "plumbing",
            "pack": "JM",
            "module": "rule_1302004",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1302008": {
            "major": "plumbing",
            "pack": "JM",
            "module": "rule_1302008",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1302007": {
            "major": "plumbing",
            "pack": "JM",
            "module": "rule_1302007",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1302009": {
            "major": "plumbing",
            "pack": "JM",
            "module": "rule_1302009",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1302010": {
            "major": "plumbing",
            "pack": "JM",
            "module": "rule_1302010",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1302012": {
            "major": "plumbing",
            "pack": "JM",
            "module": "rule_1302012",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1302014": {
            "major": "plumbing",
            "pack": "JM",
            "module": "rule_1302014",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1302016": {
            "major": "plumbing",
            "pack": "JM",
            "module": "rule_1302016",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1302018": {
            "major": "plumbing",
            "pack": "JM",
            "module": "rule_1302018",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        # 暖通跨图框:
        "1402001": {
            "major": "hvac",
            "pack": "JM",
            "module": "rule_1402001",
            "class_name": "Rule",
            "checkpoint_amount": 5,
        },
        "1402002": {
            "major": "hvac",
            "pack": "JM",
            "module": "rule_1402002",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1402005": {
            "major": "hvac",
            "pack": "JM",
            "module": "rule_1402005",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1402007": {
            "major": "hvac",
            "pack": "JM",
            "module": "rule_1402007",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1402008": {
            "major": "hvac",
            "pack": "JM",
            "module": "rule_1402008",
            "class_name": "Rule",
            "checkpoint_amount": 4,
        },
        "1402009": {
            "major": "hvac",
            "pack": "JM",
            "module": "rule_1402009",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },

        "1402014": {
            "major": "hvac",
            "pack": "JM",
            "module": "rule_1402014",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1402013": {
            "major": "hvac",
            "pack": "JM",
            "module": "rule_1402013",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1402017": {
            "major": "hvac",
            "pack": "JM",
            "module": "rule_1402017",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1402024": {
            "major": "hvac",
            "pack": "JM",
            "module": "rule_1402024",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1402027": {
            "major": "hvac",
            "pack": "JM",
            "module": "rule_1402024",
            "class_name": "Rule",
            "checkpoint_amount": 3,
        },
        "1404001": {
            "major": "hvac",
            "pack": "ZH",
            "module": "rule_1404001",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        # 电气单图框
        "1500001": {
            "major": "electric",
            "pack": "PL",
            "module": "rule_1500001",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1502006": {
            "major": "electric",
            "pack": "JM",
            "module": "rule_1502006",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1502007": {
            "major": "electric",
            "pack": "JM",
            "module": "rule_1502007",
            "class_name": "Rule",
            "checkpoint_amount": 3,
        },
        "1502008": {
            "major": "electric",
            "pack": "JM",
            "module": "rule_1502008",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1502009": {
            "major": "electric",
            "pack": "JM",
            "module": "rule_1502009",
            "class_name": "Rule",
            "checkpoint_amount": 4,
        },
        "1502001": {
            "major": "electric",
            "pack": "JM",
            "module": "rule_1502001",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1502002": {
            "major": "electric",
            "pack": "JM",
            "module": "rule_1502002",
            "class_name": "Rule",
            "checkpoint_amount": 3,
        },
        "1502003": {
            "major": "electric",
            "pack": "JM",
            "module": "rule_1502003",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1502004": {
            "major": "electric",
            "pack": "JM",
            "module": "rule_1502004",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1502005": {
            "major": "electric",
            "pack": "JM",
            "module": "rule_1502005",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1502010": {
            "major": "electric",
            "pack": "JM",
            "module": "rule_1502010",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1502012": {
            "major": "electric",
            "pack": "JM",
            "module": "rule_1502012",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1502013": {
            "major": "electric",
            "pack": "JM",
            "module": "rule_1502013",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1502014": {
            "major": "electric",
            "pack": "JM",
            "module": "rule_1502014",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1502016": {
            "major": "electric",
            "pack": "JM",
            "module": "rule_1502016",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1502017": {
            "major": "electric",
            "pack": "JM",
            "module": "rule_1502017",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1502020": {
            "major": "electric",
            "pack": "JM",
            "module": "rule_1502020",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1502021": {
            "major": "electric",
            "pack": "JM",
            "module": "rule_1502021",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1502029": {
            "major": "electric",
            "pack": "JM",
            "module": "rule_1502029",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1502030": {
            "major": "electric",
            "pack": "JM",
            "module": "rule_1502030",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        # 电气跨图框
        "1502011": {
            "major": "electric",
            "pack": "JM",
            "module": "rule_1502011",
            "class_name": "Rule",
            "checkpoint_amount": 4,
        },
        "1502019": {
            "major": "electric",
            "pack": "JM",
            "module": "rule_1502019",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1502022": {
            "major": "electric",
            "pack": "JM",
            "module": "rule_1502022",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1502023": {
            "major": "electric",
            "pack": "JM",
            "module": "rule_1502023",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1502028": {
            "major": "electric",
            "pack": "JM",
            "module": "rule_1502028",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        # 碧桂园货板稽查电气规则
        "1503001": {
            "major": "electric",
            "pack": "BGY",
            "module": "rule_1503001",
            "class_name": "Rule",
            "checkpoint_amount": 1
        },
        "1503002": {
            "major": "electric",
            "pack": "BGY",
            "module": "rule_1503002",
            "class_name": "Rule",
            "checkpoint_amount": 1
        },
        # 碧桂园货板稽查建筑规则一
        "1103001": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103001",
            "class_name": "Rule",
            "checkpoint_amount": 1
        },
        # 碧桂园货板稽查建筑规则二
        "1103002": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103002",
            "class_name": "Rule",
            "checkpoint_amount": 1
        },
        "1103003": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103003",
            "class_name": "Rule",
            "checkpoint_amount": 1
        },
        "1103004": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103004",
            "class_name": "Rule",
            "checkpoint_amount": 1
        },
        "1103005": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103005",
            "class_name": "Rule",
            "checkpoint_amount": 1
        },
        "1603001": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1603001",
            "class_name": "Rule",
            "checkpoint_amount": 1
        },

        # 品览规则
        "1300010": {
            "major": "plumbing",
            "pack": "PL",
            "module": "rule_1300010",
            "class_name": "Rule",
            "checkpoint_amount": 1
        },
        "1300012": {
            "major": "plumbing",
            "pack": "PL",
            "module": "rule_1300012",
            "class_name": "Rule",
            "checkpoint_amount": 1
        },
        "1300013": {
            "major": "plumbing",
            "pack": "PL",
            "module": "rule_1300013",
            "class_name": "Rule",
            "checkpoint_amount": 1
        },
        "1300015": {
            "major": "plumbing",
            "pack": "PL",
            "module": "rule_1300015",
            "class_name": "Rule",
            "checkpoint_amount": 1
        },
        "1300016": {
            "major": "plumbing",
            "pack": "PL",
            "module": "rule_1300016",
            "class_name": "Rule",
            "checkpoint_amount": 1
        },
        "1300017": {
            "major": "plumbing",
            "pack": "PL",
            "module": "rule_1300017",
            "class_name": "Rule",
            "checkpoint_amount": 1
        },
        "1300025": {
            "major": "plumbing",
            "pack": "PL",
            "module": "rule_1300025",
            "class_name": "Rule",
            "checkpoint_amount": 2
        },
        "1300005": {
            "major": "plumbing",
            "pack": "PL",
            "module": "rule_1300005",
            "class_name": "Rule",
            "checkpoint_amount": 1
        },
        "1300004": {
            "major": "plumbing",
            "pack": "PL",
            "module": "rule_1300004",
            "class_name": "Rule",
            "checkpoint_amount": 1
        },
        "1500003": {
            "major": "electric",
            "pack": "PL",
            "module": "rule_1500003",
            "class_name": "Rule",
            "checkpoint_amount": 1
        },
        "1500002": {
            "major": "electric",
            "pack": "PL",
            "module": "rule_1500002",
            "class_name": "Rule",
            "checkpoint_amount": 1
        },
        "1500004": {
            "major": "electric",
            "pack": "PL",
            "module": "rule_1500004",
            "class_name": "Rule",
            "checkpoint_amount": 1
        },

        "1302013": {
            "major": "plumbing",
            "pack": "JM",
            "module": "rule_1302013",
            "class_name": "Rule",
            "checkpoint_amount": 1
        },

        "1302011": {
            "major": "plumbing",
            "pack": "JM",
            "module": "rule_1302011",
            "class_name": "Rule",
            "checkpoint_amount": 2
        },

        "1302006": {
            "major": "plumbing",
            "pack": "JM",
            "module": "rule_1302006",
            "class_name": "Rule",
            "checkpoint_amount": 1
        },

        "1302017": {
            "major": "plumbing",
            "pack": "JM",
            "module": "rule_1302017",
            "class_name": "Rule",
            "checkpoint_amount": 1
        },

        "1302015": {
            "major": "plumbing",
            "pack": "JM",
            "module": "rule_1302015",
            "class_name": "Rule",
            "checkpoint_amount": 1
        },

        "1300028": {
            "major": "plumbing",
            "pack": "PL",
            "module": "rule_1300028",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },

        "1300026": {
            "major": "plumbing",
            "pack": "PL",
            "module": "rule_1300026",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },

        "1300030": {
            "major": "plumbing",
            "pack": "PL",
            "module": "rule_1300030",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },

        "1300032": {
            "major": "plumbing",
            "pack": "PL",
            "module": "rule_1300032",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1500037": {
            "major": "electric",
            "pack": "PL",
            "module": "rule_1500037",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1500042": {
            "major": "electric",
            "pack": "PL",
            "module": "rule_1500042",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1500047": {
            "major": "electric",
            "pack": "PL",
            "module": "rule_1500047",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1500050": {
            "major": "electric",
            "pack": "PL",
            "module": "rule_1500050",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104006": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104006",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1104005": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104005",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1104015": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104015",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104019": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104019",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104020": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104020",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104021": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104021",
            "class_name": "Rule",
            "checkpoint_amount": 3,
        },
        "1104027": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104027",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104031": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104031",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104033": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104033",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104043": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104043",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104048": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104048",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104007": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104007",
            "class_name": "Rule",
            "checkpoint_amount": 3,
        },
        "1104008": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104008",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1104018": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104018",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104046": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104046",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104054": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104054",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1104029": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104029",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104037": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104037",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104028": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104028",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104030": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104030",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1104024": {
            "major": "architecture",
            "pack": "ZH",
            "module": "rule_1104024",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1504001": {
            "major": "electric",
            "pack": "ZH",
            "module": "rule_1504001",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1304001": {
            "major": "plumbing",
            "pack": "ZH",
            "module": "rule_1304001",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },

    }


# --- Deprecated ---


class RuleEngineV2:
    SINGLE_BORDER_RULE_PATH = "rule_engine.single_border_rule"
    MULTI_BORDER_RULE_PATH = "rule_engine.multi_border_rule"
    RULE_CLASS_NAME = "Rule"
    RULE = {
        # 建筑单图框
        103061: {
            "class": "rule_103061",
            "checkpoint_amount": 2,
        },
        103080: {
            "class": "rule_103080",
            "checkpoint_amount": 1,
        },
        105015: {
            "class": "rule_105015",
            "checkpoint_amount": 2,
        },
        103070: {
            "class": "rule_103070",
            "checkpoint_amount": 1,
        },
        111003: {
            "class": "rule_111003",
            "checkpoint_amount": 3,
        },
        107011: {
            "class": "rule_107011",
            "checkpoint_amount": 1,
        },
        101001: {
            "class": "rule_101001",
            "checkpoint_amount": 1,
        },
        111001: {
            "class": "rule_111001",
            "checkpoint_amount": 1,
        },
        101002: {
            "class": "rule_101002",
            "checkpoint_amount": 1,
        },
        101003: {
            "class": "rule_101003",
            "checkpoint_amount": 1,
        },
        101004: {
            "class": "rule_101004",
            "checkpoint_amount": 1,
        },
        101005: {
            "class": "rule_101005",
            "checkpoint_amount": 1,
        },
        101006: {  # 规则6返回两个审核结果
            "class": "rule_101006",
            "checkpoint_amount": 2,
        },
        101007: {  # 规则7返回两个审核结果
            "class": "rule_101007",
            "checkpoint_amount": 2,
        },
        101008: {  # 规则8和9合并为一个函数
            "class": "rule_101008",
            "checkpoint_amount": 1,
        },
        101009: {  # 规则8和9合并为一个函数，此处占位
            "class": "rule_101008",
            "checkpoint_amount": 1,
        },
        118001: {
            "class": "rule_118001",
            "checkpoint_amount": 1,
        },
        118003: {
            "class": "rule_118003",
            "checkpoint_amount": 1,
        },
        101010: {
            "class": "rule_101010",
            "checkpoint_amount": 1,
        },
        101011: {
            "class": "rule_101011",
            "checkpoint_amount": 1,
        },
        101012: {
            "class": "rule_101012",
            "checkpoint_amount": 1,
        },
        101013: {
            "class": "rule_101013",
            "checkpoint_amount": 1,
        },
        101014: {
            "class": "rule_101014",
            "checkpoint_amount": 1,
        },
        101015: {
            "class": "rule_101015",
            "checkpoint_amount": 1,
        },
        101016: {
            "class": "rule_101016",
            "checkpoint_amount": 2,
        },
        101017: {
            "class": "rule_101017",
            "checkpoint_amount": 1,
        },
        101018: {
            "class": "rule_101018",
            "checkpoint_amount": 1,
        },
        101019: {
            "class": "rule_101019",
            "checkpoint_amount": 1,
        },
        101020: {
            "class": "rule_101020",
            "checkpoint_amount": 3,
        },
        101021: {
            "class": "rule_101021",
            "checkpoint_amount": 1,
        },
        101022: {
            "class": "rule_101022",
            "checkpoint_amount": 1,
        },
        101023: {
            "class": "rule_101022",
            "checkpoint_amount": 1,
        },
        101024: {
            "class": "rule_101024",
            "checkpoint_amount": 1,
        },
        101025: {
            "class": "rule_101025",
            "checkpoint_amount": 1,
        },
        101026: {
            "class": "rule_101026",
            "checkpoint_amount": 2,
        },
        101027: {
            "class": "rule_101027_101031_101032_101033_101034",
            "checkpoint_amount": 1,
        },
        101031: {
            "class": "rule_101027_101031_101032_101033_101034",
            "checkpoint_amount": 1,
        },
        101032: {
            "class": "rule_101027_101031_101032_101033_101034",
            "checkpoint_amount": 1,
        },
        101033: {
            "class": "rule_101027_101031_101032_101033_101034",
            "checkpoint_amount": 1,
        },
        101034: {
            "class": "rule_101027_101031_101032_101033_101034",
            "checkpoint_amount": 1,
        },
        101028: {
            "class": "rule_101028",
            "checkpoint_amount": 1,
        },
        101029: {
            "class": "rule_101029",
            "checkpoint_amount": 1,
        },
        101030: {
            "class": "rule_101030",
            "checkpoint_amount": 1,
        },
        101035: {
            "class": "rule_101035",
            "checkpoint_amount": 2,
        },
        101036: {
            "class": "rule_101036",
            "checkpoint_amount": 1,
        },
        101037: {
            "class": "rule_101037",
            "checkpoint_amount": 1,
        },
        101038: {
            "class": "rule_101038",
            "checkpoint_amount": 1,
        },
        101039: {
            "class": "rule_101039",
            "checkpoint_amount": 1,
        },
        101040: {
            "class": "rule_101040",
            "checkpoint_amount": 1,
        },
        101041: {
            "class": "rule_101041",
            "checkpoint_amount": 1,
        },
        101042: {
            "class": "rule_101042",
            "checkpoint_amount": 1,
        },
        101043: {
            "class": "rule_101043",
            "checkpoint_amount": 1,
        },
        101044: {
            "class": "rule_101044",
            "checkpoint_amount": 1,
        },
        101045: {
            "class": "rule_101045",
            "checkpoint_amount": 1,
        },
        101046: {
            "class": "rule_101046",
            "checkpoint_amount": 1,
        },
        101047: {
            "class": "rule_101047",
            "checkpoint_amount": 1,
        },
        101048: {
            "class": "rule_101048",
            "checkpoint_amount": 1,
        },
        101049: {
            "class": "rule_101049",
            "checkpoint_amount": 1,
        },
        101050: {
            "class": "rule_101050",
            "checkpoint_amount": 1,
        },
        101076: {
            "class": "rule_101076",
            "checkpoint_amount": 1,
        },
        101077: {
            "class": "rule_101077",
            "checkpoint_amount": 1,
        },
        101079: {
            "class": "rule_101079",
            "checkpoint_amount": 1,
        },
        101080: {
            "class": "rule_101080",
            "checkpoint_amount": 1,
        },
        101081: {
            "class": "rule_101081",
            "checkpoint_amount": 2,
        },
        102001: {
            "class": "rule_102001",
            "checkpoint_amount": 3,
        },
        102002: {
            "class": "rule_102002",
            "checkpoint_amount": 1,
        },
        102003: {
            "class": "rule_102003",
            "checkpoint_amount": 1,
        },
        102005: {
            "class": "rule_102005",
            "checkpoint_amount": 1,
        },
        102007: {
            "class": "rule_102007",
            "checkpoint_amount": 1,
        },
        102009: {
            "class": "rule_102009",
            "checkpoint_amount": 1,
        },
        102015: {
            "class": "rule_102015",
            "checkpoint_amount": 7,
        },
        # 85.1: {
        #     "class": "rule_85a",
        #     "checkpoint_amount": 5,
        # },
        # 85.2: {
        #     "class": "rule_85b",
        #     "checkpoint_amount": 1,
        # },
        # 85.2: {
        #     "class": "rule_85c",
        #     "checkpoint_amount": 1,
        # },
        101051: {
            "class": "rule_101051",
            "checkpoint_amount": 1,
        },
        101052: {
            "class": "rule_101052",
            "checkpoint_amount": 1,
        },
        101053: {
            "class": "rule_101053",
            "checkpoint_amount": 1,
        },
        101054: {
            "class": "rule_101054",
            "checkpoint_amount": 1,
        },
        101055: {
            "class": "rule_101055_101056",
            "checkpoint_amount": 1,
        },
        101056: {
            "class": "rule_101055_101056",
            "checkpoint_amount": 2,
        },
        101057: {
            "class": "rule_101057",
            "checkpoint_amount": 1,
        },
        101058: {
            "class": "rule_101058",
            "checkpoint_amount": 1,
        },
        101059: {
            "class": "rule_101059",
            "checkpoint_amount": 1,
        },
        101060: {
            "class": "rule_101060",
            "checkpoint_amount": 1,
        },
        101061: {
            "class": "rule_101061",
            "checkpoint_amount": 1,
        },
        101062: {
            "class": "rule_101062",
            "checkpoint_amount": 1,
        },
        101063: {
            "class": "rule_101063",
            "checkpoint_amount": 1,
        },
        101064: {
            "class": "rule_101064",
            "checkpoint_amount": 3,
        },
        101065: {
            "class": "rule_101065",
            "checkpoint_amount": 1,
        },
        104001: {
            "class": "rule_104001",
            "checkpoint_amount": 2,
        },
        104002: {
            "class": "rule_104002",
            "checkpoint_amount": 2,
        },
        104003: {
            "class": "rule_104003",
            "checkpoint_amount": 1,
        },
        104008: {
            "class": "rule_104008",
            "checkpoint_amount": 1,
        },
        104009: {
            "class": "rule_104009",
            "checkpoint_amount": 2,
        },
        102016: {
            "class": "rule_102016",
            "checkpoint_amount": 2,
        },
        102008: {
            "class": "rule_102008",
            "checkpoint_amount": 1,
        },
        103001: {
            "class": "rule_103001",
            "checkpoint_amount": 1,
        },
        103003: {
            "class": "rule_103003",
            "checkpoint_amount": 1,
        },
        103006: {
            "class": "rule_103006",
            "checkpoint_amount": 1,
        },
        104004: {
            "class": "rule_104004",
            "checkpoint_amount": 1,
        },
        104005: {
            "class": "rule_104005",
            "checkpoint_amount": 4,
        },
        104006: {
            "class": "rule_104006",
            "checkpoint_amount": 1,
        },
        103002: {
            "class": "rule_103002",
            "checkpoint_amount": 2,
        },
        103004: {
            "class": "rule_103004",
            "checkpoint_amount": 1,
        },
        103005: {
            "class": "rule_103005",
            "checkpoint_amount": 1,
        },
        103066: {
            "class": "rule_103066",
            "checkpoint_amount": 2,
        },
        104020: {
            "class": "rule_104020",
            "checkpoint_amount": 2,
        },
        103067: {
            "class": "rule_103067",
            "checkpoint_amount": 1,
        },
        103069: {
            "class": "rule_103069",
            "checkpoint_amount": 2,
        },
        103078: {
            "class": "rule_103078",
            "checkpoint_amount": 1,
        },
        103068: {
            "class": "rule_103068",
            "checkpoint_amount": 1,
        },
        103072: {
            "class": "rule_103072",
            "checkpoint_amount": 2,
        },
        103076: {
            "class": "rule_103076",
            "checkpoint_amount": 1,
        },
        104007: {
            "class": "rule_104007",
            "checkpoint_amount": 4,
        },
        104018: {
            "class": "rule_104018",
            "checkpoint_amount": 1,
        },
        104019: {
            "class": "rule_104019",
            "checkpoint_amount": 1,
        },
        104025: {
            "class": "rule_104025",
            "checkpoint_amount": 1,
        },
        104026: {
            "class": "rule_104026",
            "checkpoint_amount": 1,
        },
        104027: {
            "class": "rule_104027",
            "checkpoint_amount": 1,
        },
        104048: {
            "class": "rule_104048",
            "checkpoint_amount": 1,
        },
        104049: {
            "class": "rule_104049",
            "checkpoint_amount": 1,
        },
        103021: {
            "class": "rule_103021",
            "checkpoint_amount": 1,
        },
        103022: {
            "class": "rule_103022",
            "checkpoint_amount": 1,
        },
        103023: {
            "class": "rule_103023",
            "checkpoint_amount": 1,
        },
        103024: {
            "class": "rule_103024",
            "checkpoint_amount": 2,
        },
        103025: {
            "class": "rule_103025",
            "checkpoint_amount": 2,
        },
        103060: {
            "class": "rule_103060",
            "checkpoint_amount": 2,
        },
        103063: {
            "class": "rule_103063",
            "checkpoint_amount": 2,
        },
        105014: {
            "class": "rule_105014",
            "checkpoint_amount": 1,
        },
        107013: {
            "class": "rule_107013",
            "checkpoint_amount": 2,
        },
        107014: {
            "class": "rule_107014",
            "checkpoint_amount": 2,
        },
        103071: {
            "class": "rule_103071",
            "checkpoint_amount": 2,
        },
        103012: {
            "class": "rule_103012",
            "checkpoint_amount": 1,
        },
        103013: {
            "class": "rule_103013",
            "checkpoint_amount": 1,
        },
        103014: {
            "class": "rule_103014",
            "checkpoint_amount": 1,
        },
        103015: {
            "class": "rule_103015",
            "checkpoint_amount": 2,
        },
        103016: {
            "class": "rule_103016",
            "checkpoint_amount": 1,
        },
        103017: {
            "class": "rule_103017",
            "checkpoint_amount": 1,
        },
        103018: {
            "class": "rule_103018",
            "checkpoint_amount": 7,
        },
        103019: {
            "class": "rule_103019",
            "checkpoint_amount": 1,
        },
        103020: {
            "class": "rule_103020",
            "checkpoint_amount": 1,
        },
        103077: {
            "class": "rule_103077",
            "checkpoint_amount": 1,
        },
        104011: {
            "class": "rule_104011",
            "checkpoint_amount": 1,
        },
        104016: {
            "class": "rule_104016",
            "checkpoint_amount": 1,
        },
        104053: {
            "class": "rule_104053",
            "checkpoint_amount": 1,
        },
        107001: {
            "class": "rule_107001",
            "checkpoint_amount": 1,
        },
        107003: {
            "class": "rule_107003",
            "checkpoint_amount": 1,
        },
        107004: {
            "class": "rule_107004",
            "checkpoint_amount": 1,
        },
        111002: {
            "class": "rule_111002",
            "checkpoint_amount": 1,
        },
        104024: {
            "class": "rule_104024",
            "checkpoint_amount": 3,
        },
        104028: {
            "class": "rule_104028",
            "checkpoint_amount": 1,
        },
        106015: {
            "class": "rule_106015",
            "checkpoint_amount": 6,
        },
        111004: {
            "class": "rule_111004",
            "checkpoint_amount": 2,
        },
        105001: {
            "class": "rule_105001",
            "checkpoint_amount": 1,
        },
        # # 514: {
        # #     "rule_id": 514,
        # #     "func": rule_514.run,
        # #     "return_cnt": 2,
        # #     "abnormal_cause_id": [],    #to jiangda
        # #     "checkpoint_response": False
        # # },
        # # 515: {
        # #     "rule_id": 515,
        # #     "func": rule_515.run,
        # #     "return_cnt": 1,
        # #     "abnormal_cause_id": [],    #to jiangda
        # #     "checkpoint_response": False
        # # },
        105002: {
            "class": "rule_105002",
            "checkpoint_amount": 3,
        },
        105004: {
            "class": "rule_105004",
            "checkpoint_amount": 2,
        },
        105008: {
            "class": "rule_105008",
            "checkpoint_amount": 1,
        },
        106013: {
            "class": "rule_106013",
            "checkpoint_amount": 2,
        },
        107005: {
            "class": "rule_107005",
            "checkpoint_amount": 1,
        },
        107015: {
            "class": "rule_107015",
            "checkpoint_amount": 1,
        },
        103026: {
            "class": "rule_103026",
            "checkpoint_amount": 1,
        },
        108002: {
            "class": "rule_108002",
            "checkpoint_amount": 1,
        },
        108003: {
            "class": "rule_108003",
            "checkpoint_amount": 1,
        },
        114001: {
            "class": "rule_114001",
            "checkpoint_amount": 1,
        },
        105005: {
            "class": "rule_105005",
            "checkpoint_amount": 2,
        },
        105006: {
            "class": "rule_105006",
            "checkpoint_amount": 1,
        },
        104034: {
            "class": "rule_104034",
            "checkpoint_amount": 1,
        },
        104037: {
            "class": "rule_104037",
            "checkpoint_amount": 3,
        },
        104038: {
            "class": "rule_104038",
            "checkpoint_amount": 1,
        },
        104039: {
            "class": "rule_104039",
            "checkpoint_amount": 1,
        },
        104040: {
            "class": "rule_104040",
            "checkpoint_amount": 4,
        },
        104041: {
            "class": "rule_104041",
            "checkpoint_amount": 4,
        },
        103034: {
            "class": "rule_103034",
            "checkpoint_amount": 2,
        },
        103035: {
            "class": "rule_103035",
            "checkpoint_amount": 4,
        },
        103007: {
            "class": "rule_103007",
            "checkpoint_amount": 1,
        },
        103008: {
            "class": "rule_103008",
            "checkpoint_amount": 1,
        },
        103009: {
            "class": "rule_103009",
            "checkpoint_amount": 1,
        },
        103010: {
            "class": "rule_103010",
            "checkpoint_amount": 1,
        },
        119001: {
            "class": "rule_119001",
            "checkpoint_amount": 1,
        },
        119003: {
            "class": "rule_119003",
            "checkpoint_amount": 1,
        },
        119006: {
            "class": "rule_119006",
            "checkpoint_amount": 2,
        },
        119007: {
            "class": "rule_119007",
            "checkpoint_amount": 2,
        },
        119008: {
            "class": "rule_119008",
            "checkpoint_amount": 1,
        },
        119009: {
            "class": "rule_119009",
            "checkpoint_amount": 1,
        },
        107006: {
            "class": "rule_107006",
            "checkpoint_amount": 1,
        },
        107007: {
            "class": "rule_107007",
            "checkpoint_amount": 2,
        },
        103036: {
            "class": "rule_103036",
            "checkpoint_amount": 5,
        },
        103037: {
            "class": "rule_103037",
            "checkpoint_amount": 4,
        },
        103038: {
            "class": "rule_103038",
            "checkpoint_amount": 1,
        },
        106004: {
            "class": "rule_106004",
            "checkpoint_amount": 6,
        },
        106005: {
            "class": "rule_106005",
            "checkpoint_amount": 2,
        },
        106006: {
            "class": "rule_106006",
            "checkpoint_amount": 9,
        },
        103039: {
            "class": "rule_103039",
            "checkpoint_amount": 1,
        },
        103041: {
            "class": "rule_103041",
            "checkpoint_amount": 2,
        },
        103042: {
            "class": "rule_103042",
            "checkpoint_amount": 2,
        },
        103043: {
            "class": "rule_103043",
            "checkpoint_amount": 1,
        },
        103044: {
            "class": "rule_103044",
            "checkpoint_amount": 2,
        },
        103045: {
            "class": "rule_103045",
            "checkpoint_amount": 1,
        },
        103046: {
            "class": "rule_103046",
            "checkpoint_amount": 5,
        },
        103047: {
            "class": "rule_103047",
            "checkpoint_amount": 3,
        },
        103056: {
            "class": "rule_103056",
            "checkpoint_amount": 2,
        },
        106007: {
            "class": "rule_106007",
            "checkpoint_amount": 2,
        },
        106008: {
            "class": "rule_106008",
            "checkpoint_amount": 5,
        },
        103048: {
            "class": "rule_103048",
            "checkpoint_amount": 2,
        },
        103049: {
            "class": "rule_103049",
            "checkpoint_amount": 2,
        },
        103050: {
            "class": "rule_103050",
            "checkpoint_amount": 5,
        },
        103051: {
            "class": "rule_103051",
            "checkpoint_amount": 2,
        },
        103052: {
            "class": "rule_103052",
            "checkpoint_amount": 3,
        },
        104042: {
            "class": "rule_104042",
            "checkpoint_amount": 1,
        },
        104043: {
            "class": "rule_104043",
            "checkpoint_amount": 1,
        },
        107008: {
            "class": "rule_107008",
            "checkpoint_amount": 1,
        },
        105007: {
            "class": "rule_105007",
            "checkpoint_amount": 1,
        },
        117001: {
            "class": "rule_117001",
            "checkpoint_amount": 1,
        },
        106001: {
            "class": "rule_106001",
            "checkpoint_amount": 6,
        },
        106009: {
            "class": "rule_106009",
            "checkpoint_amount": 5,
        },
        106021: {
            "class": "rule_106021",
            "checkpoint_amount": 1,
        },
        106027: {
            "class": "rule_106027",
            "checkpoint_amount": 2,
        },
        103055: {
            "class": "rule_103055",
            "checkpoint_amount": 1,
        },
        105013: {
            "class": "rule_105013",
            "checkpoint_amount": 9,
        },
        105017: {
            "class": "rule_105017",
            "checkpoint_amount": 2,
        },
        108004: {
            "class": "rule_108004",
            "checkpoint_amount": 3,
        },
        106031: {
            "class": "rule_106031",
            "checkpoint_amount": 1,
        },
        106016: {
            "class": "rule_106016",
            "checkpoint_amount": 2,
        },
        106018: {
            "class": "rule_106018",
            "checkpoint_amount": 2,
        },
        106019: {
            "class": "rule_106019",
            "checkpoint_amount": 4,
        },
        107010: {
            "class": "rule_107010",
            "checkpoint_amount": 3,
        },
        # 建筑跨图框
        # # 515: {
        # #     "rule_id": 652,
        # #     "func": rule_515.run,
        # #     "return_cnt": 1,
        # #     "abnormal_cause_id": [],     #to jiangda
        # #     "checkpoint_response": False
        # # },
        105016: {
            "class": "rule_105016",
            "checkpoint_amount": 1,
        },
        104030: {
            "class": "rule_104030",
            "checkpoint_amount": 1,
        },
        106002: {
            "class": "rule_106002",
            "checkpoint_amount": 1,
        },
        104031: {
            "class": "rule_104031",
            "checkpoint_amount": 1,
        },
        104032: {
            "class": "rule_104032",
            "checkpoint_amount": 5,
        },
        104033: {
            "class": "rule_104033",
            "checkpoint_amount": 1,
        },
        104035: {
            "class": "rule_104035",
            "checkpoint_amount": 1,
        },
        104036: {
            "class": "rule_104036",
            "checkpoint_amount": 3,
        },
        103027: {
            "class": "rule_103027",
            "checkpoint_amount": 1,
        },
        103028: {
            "class": "rule_103028",
            "checkpoint_amount": 1,
        },
        103029: {
            "class": "rule_103029",
            "checkpoint_amount": 1,
        },
        103030: {
            "class": "rule_103030",
            "checkpoint_amount": 2,
        },
        103031: {
            "class": "rule_103031",
            "checkpoint_amount": 1,
        },
        106003: {
            "class": "rule_106003",
            "checkpoint_amount": 3,
        },
        103033: {
            "class": "rule_103033",
            "checkpoint_amount": 3,
        },
        103032: {
            "class": "rule_103032",
            "checkpoint_amount": 2,
        },
        108005: {
            "class": "rule_108005",
            "checkpoint_amount": 2,
        },
        109001: {
            "class": "rule_109001",
            "checkpoint_amount": 2,
        },
        109002: {
            "class": "rule_109002",
            "checkpoint_amount": 2,
        },
        109003: {
            "class": "rule_109003",
            "checkpoint_amount": 2,
        },
        109004: {
            "class": "rule_109004",
            "checkpoint_amount": 2,
        },
        103040: {
            "class": "rule_103040",
            "checkpoint_amount": 1,
        },
        110001: {
            "class": "rule_110001",
            "checkpoint_amount": 3,
        },
        110002: {
            "class": "rule_110002",
            "checkpoint_amount": 3,
        },
        110003: {
            "class": "rule_110003",
            "checkpoint_amount": 3,
        },
        119004: {
            "class": "rule_119004",
            "checkpoint_amount": 1,
        },
        103053: {
            "class": "rule_103053",
            "checkpoint_amount": 3,
        },
        103054: {
            "class": "rule_103054",
            "checkpoint_amount": 3,
        },
        106010: {
            "class": "rule_106010",
            "checkpoint_amount": 4,
        },
        106011: {
            "class": "rule_106011",
            "checkpoint_amount": 3,
        },
        106012: {
            "class": "rule_106012",
            "checkpoint_amount": 2,
        },
        115001: {
            "class": "rule_115001",
            "checkpoint_amount": 1,
        },
        # 104023: {
        #     "rule_id": 279,
        #     "func": rule_160.run,
        #     "return_cnt": 1,
        #     "abnormal_cause_id": [],     #to jiangda
        #     "checkpoint_response": False
        # },
        104022: {
            "class": "rule_104022",
            "checkpoint_amount": 1,
        },
        104023: {
            "class": "rule_104023",
            "checkpoint_amount": 1,
        },
        104029: {
            "class": "rule_104029",
            "checkpoint_amount": 1,
        },
        110004: {
            "class": "rule_110004",
            "checkpoint_amount": 6,
        },
        110005: {
            "class": "rule_110005",
            "checkpoint_amount": 3,
        },
        110006: {
            "class": "rule_110006",
            "checkpoint_amount": 3,
        },
        110007: {
            "class": "rule_110007",
            "checkpoint_amount": 3,
        },
        112001: {
            "class": "rule_112001",
            "checkpoint_amount": 1,
        },
        106025: {
            "class": "rule_106025",
            "checkpoint_amount": 11,
        },
        106026: {
            "class": "rule_106026",
            "checkpoint_amount": 4,
        },
        104051: {
            "class": "rule_104051",
            "checkpoint_amount": 1,
        },
        110008: {
            "class": "rule_110008",
            "checkpoint_amount": 1,
        },
        103065: {
            "class": "rule_103065",
            "checkpoint_amount": 4,
        },
        103073: {
            "class": "rule_103073",
            "checkpoint_amount": 4,
        },
        108009: {
            "class": "rule_108009",
            "checkpoint_amount": 1,
        },
        103075: {
            "class": "rule_103075",
            "checkpoint_amount": 1,
        },
        104054: {
            "class": "rule_104054",
            "checkpoint_amount": 3,
        },
        106022: {
            "class": "rule_106022",
            "checkpoint_amount": 3,
        },
        # 110008: {
        #     "rule_id": 615,
        #     "func": rule_615.run,
        #     "return_cnt": 1,
        #     "abnormal_cause_id": [],     #to jiangda
        #     "checkpoint_response": False
        # },
        # 103065: {
        #     "class": "rule_103065",
        #     "checkpoint_amount": 4,
        # },
        # 103069: {
        #     "class": "rule_103069",
        #     "checkpoint_amount": 2,
        # },
        # 103073: {
        #     "class": "rule_103073",
        #     "checkpoint_amount": 4,
        # },
        119002: {
            "class": "rule_119002",
            "checkpoint_amount": 1,
        },
        119005: {
            "class": "rule_119005",
            "checkpoint_amount": 1,
        },
        103011: {
            "class": "rule_103011",
            "checkpoint_amount": 1,
        },
        104012: {
            "class": "rule_104012",
            "checkpoint_amount": 1,
        },
        104013: {
            "class": "rule_104013",
            "checkpoint_amount": 1,
        },
        104014: {
            "class": "rule_104014",
            "checkpoint_amount": 1,
        },
        104015: {
            "class": "rule_104015",
            "checkpoint_amount": 1,
        },
        104017: {
            "class": "rule_104017",
            "checkpoint_amount": 1,
        },
        104010: {
            "class": "rule_104010",
            "checkpoint_amount": 1,
        },
        107002: {
            "class": "rule_107002",
            "checkpoint_amount": 1,
        },
        113001: {
            "class": "rule_113001",
            "checkpoint_amount": 1,
        },
        118002: {
            "class": "rule_118002",
            "checkpoint_amount": 1,
        },
        # 给排水单图框
        301003: {
            "class": "rule_301003",
            "checkpoint_amount": 1,
        },
        301004: {
            "class": "rule_301004",
            "checkpoint_amount": 4,
        },
        # 301005: {
        #     "rule_id": 301005,
        #     "func": rule_301005.run,
        #     "return_cnt": 1,
        #     "abnormal_cause_id": [],
        #     "checkpoint_response": False
        # },
        116001: {
            "class": "rule_116001",
            "checkpoint_amount": 1,
        },
        116002: {
            "class": "rule_116002",
            "checkpoint_amount": 1,
        },
        108007: {
            "class": "rule_108007",
            "checkpoint_amount": 2,
        },
        301007: {
            "class": "rule_301007",
            "checkpoint_amount": 2,
        },
        302001: {
            "class": "rule_302001",
            "checkpoint_amount": 2,
        },
        302002: {
            "class": "rule_302002",
            "checkpoint_amount": 2,
        },
        302003: {
            "class": "rule_302003",
            "checkpoint_amount": 2,
        },
        302007: {
            "class": "rule_302007",
            "checkpoint_amount": 1,
        },
        303003: {
            "class": "rule_303003",
            "checkpoint_amount": 2,
        },
        303004: {
            "class": "rule_303004",
            "checkpoint_amount": 1,
        },
        303005: {
            "class": "rule_303005",
            "checkpoint_amount": 1,
        },
        303007: {
            "class": "rule_303007",
            "checkpoint_amount": 1,
        },
        303009: {
            "class": "rule_303009",
            "checkpoint_amount": 2,
        },
        303012: {
            "class": "rule_303012",
            "checkpoint_amount": 1,
        },
        303020: {
            "class": "rule_303020",
            "checkpoint_amount": 1,
        },
        303021: {
            "class": "rule_303021",
            "checkpoint_amount": 1,
        },
        303023: {
            "class": "rule_303023",
            "checkpoint_amount": 1,
        },
        303025: {
            "class": "rule_303025",
            "checkpoint_amount": 1,
        },
        303029: {
            "class": "rule_303029",
            "checkpoint_amount": 1,
        },
        303032: {
            "class": "rule_303032",
            "checkpoint_amount": 1,
        },
        303034: {
            "class": "rule_303034",
            "checkpoint_amount": 1,
        },
        303035: {
            "class": "rule_303035",
            "checkpoint_amount": 1,
        },
        303036: {
            "class": "rule_303036",
            "checkpoint_amount": 1,
        },
        303040: {
            "class": "rule_303040",
            "checkpoint_amount": 4,
        },
        303042: {
            "class": "rule_303042",
            "checkpoint_amount": 1,
        },
        303043: {
            "class": "rule_303043",
            "checkpoint_amount": 1,
        },
        303037: {
            "class": "rule_303037",
            "checkpoint_amount": 1,
        },
        303039: {
            "class": "rule_303039",
            "checkpoint_amount": 1,
        },
        305008: {
            "class": "rule_305008",
            "checkpoint_amount": 1,
        },
        305012: {
            "class": "rule_305012",
            "checkpoint_amount": 1,
        },
        305014: {
            "class": "rule_305014",
            "checkpoint_amount": 2,
        },
        305018: {
            "class": "rule_305018",
            "checkpoint_amount": 2,
        },
        306003: {
            "class": "rule_306003",
            "checkpoint_amount": 1,
        },
        # 306002: {
        #     "rule_id": 306002,
        #     "func": rule_306002.run,
        #     "return_cnt": 1,
        #     "abnormal_cause_id": [],
        #     "checkpoint_response": False
        # },
        307002: {
            "class": "rule_307002",
            "checkpoint_amount": 1,
        },
        307004: {
            "class": "rule_307004",
            "checkpoint_amount": 1,
        },
        307006: {
            "class": "rule_307006",
            "checkpoint_amount": 1,
        },
        312001: {
            "class": "rule_312001",
            "checkpoint_amount": 1,
        },
        303011: {
            "class": "rule_303011",
            "checkpoint_amount": 1,
        },
        303019: {
            "class": "rule_303019",
            "checkpoint_amount": 1,
        },
        303022: {
            "class": "rule_303022",
            "checkpoint_amount": 1,
        },
        308004: {
            "class": "rule_308004",
            "checkpoint_amount": 1,
        },
        302004: {
            "class": "rule_302004",
            "checkpoint_amount": 1,
        },
        308009: {
            "class": "rule_308009",
            "checkpoint_amount": 1,
        },
        # 给排水跨图框
        301001: {
            "class": "rule_301001",
            "checkpoint_amount": 1,
        },
        301002: {
            "class": "rule_301002",
            "checkpoint_amount": 1,
        },
        301006: {
            "class": "rule_301006",
            "checkpoint_amount": 1,
        },
        301008: {
            "class": "rule_301008",
            "checkpoint_amount": 2,
        },
        301009: {
            "class": "rule_301009",
            "checkpoint_amount": 1,
        },
        301010: {
            "class": "rule_301010",
            "checkpoint_amount": 1,
        },
        302005: {
            "class": "rule_302005",
            "checkpoint_amount": 1,
        },
        302006: {
            "class": "rule_302006",
            "checkpoint_amount": 1,
        },
        302008: {
            "class": "rule_302008",
            "checkpoint_amount": 1,
        },
        303001: {
            "class": "rule_303001",
            "checkpoint_amount": 1,
        },
        303002: {
            "class": "rule_303002",
            "checkpoint_amount": 1,
        },
        303013: {
            "class": "rule_303013",
            "checkpoint_amount": 1,
        },
        303014: {
            "class": "rule_303014",
            "checkpoint_amount": 1,
        },
        303015: {
            "class": "rule_303015",
            "checkpoint_amount": 2,
        },
        303016: {
            "class": "rule_303016",
            "checkpoint_amount": 1,
        },
        303017: {
            "class": "rule_303017",
            "checkpoint_amount": 1,
        },
        303018: {
            "class": "rule_303018",
            "checkpoint_amount": 1,
        },
        303028: {
            "class": "rule_303028",
            "checkpoint_amount": 1,
        },
        # 303031: {
        #     "rule_id": 303031,
        #     "func": rule_303031.run,
        #     "return_cnt": 3,
        #     "abnormal_cause_id": [],
        #     "checkpoint_response": False
        # },
        303033: {
            "class": "rule_303033",
            "checkpoint_amount": 3,
        },
        303038: {
            "class": "rule_303038",
            "checkpoint_amount": 1,
        },
        303046: {
            "class": "rule_303046",
            "checkpoint_amount": 1,
        },
        304001: {
            "class": "rule_304001",
            "checkpoint_amount": 1,
        },
        305001: {
            "class": "rule_305001",
            "checkpoint_amount": 2,
        },
        305002: {
            "class": "rule_305002",
            "checkpoint_amount": 3,
        },
        305003: {
            "class": "rule_305003",
            "checkpoint_amount": 2,
        },
        305004: {
            "class": "rule_305004",
            "checkpoint_amount": 1,
        },
        305005: {
            "class": "rule_305005",
            "checkpoint_amount": 1,
        },
        305006: {
            "class": "rule_305006",
            "checkpoint_amount": 1,
        },
        305007: {
            "class": "rule_305007",
            "checkpoint_amount": 1,
        },
        305009: {
            "class": "rule_305009",
            "checkpoint_amount": 1,
        },
        305010: {
            "class": "rule_305010",
            "checkpoint_amount": 1,
        },
        305015: {
            "class": "rule_305015",
            "checkpoint_amount": 1,
        },
        305016: {
            "class": "rule_305016",
            "checkpoint_amount": 1,
        },
        305017: {
            "class": "rule_305017",
            "checkpoint_amount": 1,
        },
        305019: {
            "class": "rule_305019",
            "checkpoint_amount": 1,
        },
        305020: {
            "class": "rule_305020",
            "checkpoint_amount": 1,
        },
        305022: {
            "class": "rule_305022",
            "checkpoint_amount": 2,
        },
        306001: {
            "class": "rule_306001",
            "checkpoint_amount": 1,
        },
        306002: {
            "class": "rule_306002",
            "checkpoint_amount": 1,
        },
        307001: {
            "class": "rule_307001",
            "checkpoint_amount": 1,
        },
        308001: {
            "class": "rule_308001",
            "checkpoint_amount": 1,
        },
        308002: {
            "class": "rule_308002",
            "checkpoint_amount": 1,
        },
        308003: {
            "class": "rule_308003",
            "checkpoint_amount": 1,
        },
        308005: {
            "class": "rule_308005",
            "checkpoint_amount": 1,
        },
        308006: {
            "class": "rule_308006",
            "checkpoint_amount": 1,
        },
        308007: {
            "class": "rule_308007",
            "checkpoint_amount": 1,
        },
        308008: {
            "class": "rule_308008",
            "checkpoint_amount": 1,
        },
        308010: {
            "class": "rule_308010",
            "checkpoint_amount": 1,
        },
        308011: {
            "class": "rule_308011",
            "checkpoint_amount": 3,
        },
        309001: {
            "class": "rule_309001",
            "checkpoint_amount": 1,
        },
        309002: {
            "class": "rule_309002",
            "checkpoint_amount": 1,
        },
        310001: {
            "class": "rule_310001",
            "checkpoint_amount": 1,
        },
        310002: {
            "class": "rule_310002",
            "checkpoint_amount": 2,
        },
        310003: {
            "class": "rule_310003",
            "checkpoint_amount": 1,
        },
        310004: {
            "class": "rule_310004",
            "checkpoint_amount": 1,
        },
        311001: {
            "class": "rule_311001",
            "checkpoint_amount": 1,
        },
        311002: {
            "class": "rule_311002",
            "checkpoint_amount": 1,
        },
        311003: {
            "class": "rule_311003",
            "checkpoint_amount": 1,
        },
        313001: {
            "class": "rule_313001",
            "checkpoint_amount": 1,
        },
        313002: {
            "class": "rule_313002",
            "checkpoint_amount": 1,
        },
        314001: {
            "class": "rule_314001",
            "checkpoint_amount": 2,
        },
        303010: {
            "class": "rule_303010",
            "checkpoint_amount": 2,
        },
        # 303013: {
        #     "rule_id": 303013,
        #     "func": rule_303013.run,
        #     "return_cnt": 1,
        #     "abnormal_cause_id": [],
        #     "checkpoint_response": False
        # },
        303026: {
            "class": "rule_303026",
            "checkpoint_amount": 1,
        },
        501001: {
            "class": "rule_501001",
            "checkpoint_amount": 1,
        },
        501002: {
            "class": "rule_501002",
            "checkpoint_amount": 1,
        },
        501003: {
            "class": "rule_501003",
            "checkpoint_amount": 1,
        },
        501004: {
            "class": "rule_501004",
            "checkpoint_amount": 1,
        },
        501005: {
            "class": "rule_501005",
            "checkpoint_amount": 1,
        },
        501006: {
            "class": "rule_501006",
            "checkpoint_amount": 3,
        },
        501007: {
            "class": "rule_501007",
            "checkpoint_amount": 1,
        },
        501008: {
            "class": "rule_501008",
            "checkpoint_amount": 1,
        },
        501009: {
            "class": "rule_501009",
            "checkpoint_amount": 2,
        },
        501033: {
            "class": "rule_501033",
            "checkpoint_amount": 1,
        },
        501034: {
            "class": "rule_501034",
            "checkpoint_amount": 1,
        },
        501035: {
            "class": "rule_501035",
            "checkpoint_amount": 1,
        },
        501040: {
            "class": "rule_501040",
            "checkpoint_amount": 2,
        },
        503001: {
            "class": "rule_503001",
            "checkpoint_amount": 1,
        },
        505010: {
            "class": "rule_505010",
            "checkpoint_amount": 1,
        },
        506001: {
            "class": "rule_506001",
            "checkpoint_amount": 3,
        },
        506004: {
            "class": "rule_506004",
            "checkpoint_amount": 4,
        },
        506005: {
            "class": "rule_506005",
            "checkpoint_amount": 4,
        },
        506006: {
            "class": "rule_506006",
            "checkpoint_amount": 2,
        },
        506007: {
            "class": "rule_506007",
            "checkpoint_amount": 1,
        },
        507001: {
            "class": "rule_507001",
            "checkpoint_amount": 1,
        },
        507002: {
            "class": "rule_507002",
            "checkpoint_amount": 1,
        },
        507003: {
            "class": "rule_507003",
            "checkpoint_amount": 1,
        },
        507004: {
            "class": "rule_507004",
            "checkpoint_amount": 6,
        },
        511001: {
            "class": "rule_511001",
            "checkpoint_amount": 2,
        },
        512001: {
            "class": "rule_512001",
            "checkpoint_amount": 2,
        },
        512002: {
            "class": "rule_512002",
            "checkpoint_amount": 4,
        },
        515025: {
            "class": "rule_515025",
            "checkpoint_amount": 1,
        },
        515019: {
            "class": "rule_515019",
            "checkpoint_amount": 1,
        },
        513005: {
            "class": "rule_513005",
            "checkpoint_amount": 1,
        },
        515001: {
            "class": "rule_515001",
            "checkpoint_amount": 1,
        },
        514011: {
            "class": "rule_514011",
            "checkpoint_amount": 1,
        },
        513002: {
            "class": "rule_513002",
            "checkpoint_amount": 1,
        },
        513004: {
            "class": "rule_513004",
            "checkpoint_amount": 2,
        },
        515027: {
            "class": "rule_515027",
            "checkpoint_amount": 1,
        },
        501061: {
            "class": "rule_501061",
            "checkpoint_amount": 1,
        },
        # 电气跨图框
        501010: {
            "class": "rule_501010",
            "checkpoint_amount": 2,
        },
        501011: {
            "class": "rule_501011",
            "checkpoint_amount": 1,
        },
        501012: {
            "class": "rule_501012",
            "checkpoint_amount": 1,
        },
        501013: {
            "class": "rule_501013",
            "checkpoint_amount": 1,
        },
        501014: {
            "class": "rule_501014",
            "checkpoint_amount": 1,
        },
        501015: {
            "class": "rule_501015",
            "checkpoint_amount": 1,
        },
        501016: {
            "class": "rule_501016",
            "checkpoint_amount": 1,
        },
        501017: {
            "class": "rule_501017",
            "checkpoint_amount": 1,
        },
        501018: {
            "class": "rule_501018",
            "checkpoint_amount": 1,
        },
        501019: {
            "class": "rule_501019",
            "checkpoint_amount": 1,
        },
        501020: {
            "class": "rule_501020",
            "checkpoint_amount": 1,
        },
        501021: {
            "class": "rule_501021",
            "checkpoint_amount": 1,
        },
        501022: {
            "class": "rule_501022",
            "checkpoint_amount": 1,
        },
        501023: {
            "class": "rule_501023",
            "checkpoint_amount": 1,
        },
        501024: {
            "class": "rule_501024",
            "checkpoint_amount": 1,
        },
        501025: {
            "class": "rule_501025",
            "checkpoint_amount": 1,
        },
        501026: {
            "class": "rule_501026",
            "checkpoint_amount": 1,
        },
        501027: {
            "class": "rule_501027",
            "checkpoint_amount": 1,
        },
        501028: {
            "class": "rule_501028",
            "checkpoint_amount": 1,
        },
        501029: {
            "class": "rule_501029",
            "checkpoint_amount": 1,
        },
        501030: {
            "class": "rule_501030",
            "checkpoint_amount": 1,
        },
        501031: {
            "class": "rule_501031",
            "checkpoint_amount": 1,
        },
        501032: {
            "class": "rule_501032",
            "checkpoint_amount": 1,
        },
        501036: {
            "class": "rule_501036",
            "checkpoint_amount": 1,
        },
        501038: {
            "class": "rule_501038",
            "checkpoint_amount": 3,
        },
        501043: {
            "class": "rule_501043",
            "checkpoint_amount": 1,
        },
        501044: {
            "class": "rule_501044",
            "checkpoint_amount": 1,
        },
        501045: {
            "class": "rule_501045",
            "checkpoint_amount": 1,
        },
        501046: {
            "class": "rule_501046",
            "checkpoint_amount": 1,
        },
        501047: {
            "class": "rule_501047",
            "checkpoint_amount": 1,
        },
        501048: {
            "class": "rule_501048",
            "checkpoint_amount": 1,
        },
        501049: {
            "class": "rule_501049",
            "checkpoint_amount": 1,
        },
        501050: {
            "class": "rule_501050",
            "checkpoint_amount": 1,
        },
        501051: {
            "class": "rule_501051",
            "checkpoint_amount": 1,
        },
        501055: {
            "class": "rule_501055",
            "checkpoint_amount": 1,
        },
        501056: {
            "class": "rule_501056",
            "checkpoint_amount": 2,
        },
        501052: {
            "class": "rule_501052",
            "checkpoint_amount": 1,
        },
        501054: {
            "class": "rule_501054",
            "checkpoint_amount": 1,
        },
        501057: {
            "class": "rule_501057",
            "checkpoint_amount": 1,
        },
        501058: {
            "class": "rule_501058",
            "checkpoint_amount": 1,
        },
        501059: {
            "class": "rule_501059",
            "checkpoint_amount": 1,
        },
        501060: {
            "class": "rule_501060",
            "checkpoint_amount": 1,
        },
        504001: {
            "class": "rule_504001",
            "checkpoint_amount": 1,
        },
        504002: {
            "class": "rule_504002",
            "checkpoint_amount": 1,
        },
        505001: {
            "class": "rule_505001",
            "checkpoint_amount": 4,
        },
        505002: {
            "class": "rule_505002",
            "checkpoint_amount": 1,
        },
        505003: {
            "class": "rule_505003",
            "checkpoint_amount": 1,
        },
        505004: {
            "class": "rule_505004",
            "checkpoint_amount": 1,
        },
        505005: {
            "class": "rule_505005",
            "checkpoint_amount": 1,
        },
        505006: {
            "class": "rule_505006",
            "checkpoint_amount": 1
        },
        505007: {
            "class": "rule_505007",
            "checkpoint_amount": 2
        },
        505008: {
            "class": "rule_505008",
            "checkpoint_amount": 1,
        },
        506002: {
            "class": "rule_506002",
            "checkpoint_amount": 1,
        },
        506003: {
            "class": "rule_506003",
            "checkpoint_amount": 1,
        },
        505009: {
            "class": "rule_505009",
            "checkpoint_amount": 4,
        },
        508001: {
            "class": "rule_508001",
            "checkpoint_amount": 1,
        },
        509001: {
            "class": "rule_509001",
            "checkpoint_amount": 1,
        },
        510001: {
            "class": "rule_510001",
            "checkpoint_amount": 1,
        },
        510002: {
            "class": "rule_510002",
            "checkpoint_amount": 1,
        },
        510003: {
            "class": "rule_510003",
            "checkpoint_amount": 1,
        },
        510004: {
            "class": "rule_510004",
            "checkpoint_amount": 1,
        },
        510005: {
            "class": "rule_510005",
            "checkpoint_amount": 1,
        },
        510006: {
            "class": "rule_510006",
            "checkpoint_amount": 1,
        },
        510007: {
            "class": "rule_510007",
            "checkpoint_amount": 1,
        },
        511002: {
            "class": "rule_511002",
            "checkpoint_amount": 1,
        },
        511003: {
            "class": "rule_511003",
            "checkpoint_amount": 1,
        },
        512003: {
            "class": "rule_512003",
            "checkpoint_amount": 1,
        },
        512004: {
            "class": "rule_512004",
            "checkpoint_amount": 1,
        },
        513001: {
            "class": "rule_513001",
            "checkpoint_amount": 2,
        },
        514001: {
            "class": "rule_514001",
            "checkpoint_amount": 1,
        },
        514002: {
            "class": "rule_514002",
            "checkpoint_amount": 1,
        },
        514003: {
            "class": "rule_514003",
            "checkpoint_amount": 1,
        },
        514010: {
            "class": "rule_514010",
            "checkpoint_amount": 1,
        },
        514018: {
            "class": "rule_514018",
            "checkpoint_amount": 1,
        },
        515021: {
            "class": "rule_515021",
            "checkpoint_amount": 1,
        },
        301005: {
            "class": "rule_301005",
            "checkpoint_amount": 1,
        },
        303024: {
            "class": "rule_303024",
            "checkpoint_amount": 1,
        },
        303027: {
            "class": "rule_303027",
            "checkpoint_amount": 1,
        },
        306006: {
            "class": "rule_306006",
            "checkpoint_amount": 1,
        },
        514004: {
            "class": "rule_514004",
            "checkpoint_amount": 2,
        },
        514005: {
            "class": "rule_514005",
            "checkpoint_amount": 2,
        },
        514007: {
            "class": "rule_514007",
            "checkpoint_amount": 1,
        },
        514016: {
            "class": "rule_514016",
            "checkpoint_amount": 1,
        },
        514019: {
            "class": "rule_514019",
            "checkpoint_amount": 1,
        },
        515002: {
            "class": "rule_515002",
            "checkpoint_amount": 1,
        },
        515003: {
            "class": "rule_515003",
            "checkpoint_amount": 1,
        },
        515006: {
            "class": "rule_515006",
            "checkpoint_amount": 1,
        },
        515009: {
            "class": "rule_515009",
            "checkpoint_amount": 1,
        },
        514006: {
            "class": "rule_514006",
            "checkpoint_amount": 2,
        },
        514017: {
            "class": "rule_514017",
            "checkpoint_amount": 1,
        },
        515012: {
            "class": "rule_515012",
            "checkpoint_amount": 1,
        },
        515014: {
            "class": "rule_515014",
            "checkpoint_amount": 2,
        },
        515016: {
            "class": "rule_515016",
            "checkpoint_amount": 3,
        },
        515017: {
            "class": "rule_515017",
            "checkpoint_amount": 2,
        },
        515018: {
            "class": "rule_515018",
            "checkpoint_amount": 1,
        },
        515022: {
            "class": "rule_515022",
            "checkpoint_amount": 2,
        },
        515028: {
            "class": "rule_515028",
            "checkpoint_amount": 1,
        },
        515029: {
            "class": "rule_515029",
            "checkpoint_amount": 5,
        },
        515030: {
            "class": "rule_515030",
            "checkpoint_amount": 1,
        },
        515032: {
            "class": "rule_515032",
            "checkpoint_amount": 1,
        },
        515033: {
            "class": "rule_515033",
            "checkpoint_amount": 1,
        },
        506008: {
            "class": "rule_506008",
            "checkpoint_amount": 1,
        },
        305021: {
            "class": "rule_305021",
            "checkpoint_amount": 1,
        },
        306005: {
            "class": "rule_306005",
            "checkpoint_amount": 1,
        },
        514009: {
            "class": "rule_514009",
            "checkpoint_amount": 3,
        },
        515015: {
            "class": "rule_515015",
            "checkpoint_amount": 1,
        },
        501053: {
            "class": "rule_501053",
            "checkpoint_amount": 1,
        },
        515020: {
            "class": "rule_515020",
            "checkpoint_amount": 2,
        },
        515023: {
            "class": "rule_515023",
            "checkpoint_amount": 1,
        },
        501062: {
            "class": "rule_501062",
            "checkpoint_amount": 1,
        },
        502001: {
            "class": "rule_502001",
            "checkpoint_amount": 1,
        },
        303044: {
            "class": "rule_303044",
            "checkpoint_amount": 1,
        },
        303045: {
            "class": "rule_303045",
            "checkpoint_amount": 1,
        },
        305013: {
            "class": "rule_305013",
            "checkpoint_amount": 1,
        },
        513006: {
            "class": "rule_513006",
            "checkpoint_amount": 1,
        },
        514012: {
            "class": "rule_514012",
            "checkpoint_amount": 1,
        },
        514013: {
            "class": "rule_514013",
            "checkpoint_amount": 2,
        },
        515008: {
            "class": "rule_515008",
            "checkpoint_amount": 1,
        },
        515024: {
            "class": "rule_515024",
            "checkpoint_amount": 1,
        },
        515026: {
            "class": "rule_515026",
            "checkpoint_amount": 1,
        },
        515031: {
            "class": "rule_515031",
            "checkpoint_amount": 1,
        },
        515013: {
            "class": "rule_515013",
            "checkpoint_amount": 1,
        },
        513003: {
            "class": "rule_513003",
            "checkpoint_amount": 1,
        },
        513007: {
            "class": "rule_513007",
            "checkpoint_amount": 1,
        },
        516001: {
            "class": "rule_516001",
            "checkpoint_amount": 1,
        },
        513008: {
            "class": "rule_513008",
            "checkpoint_amount": 1,
        },
        515004: {
            "class": "rule_515004",
            "checkpoint_amount": 1,
        },
        515005: {
            "class": "rule_515005",
            "checkpoint_amount": 6,
        },
        515010: {
            "class": "rule_515010",
            "checkpoint_amount": 2,
        },
        514014: {
            "class": "rule_514014",
            "checkpoint_amount": 3,
        },
        514015: {
            "class": "rule_514015",
            "checkpoint_amount": 3,
        },
        515007: {
            "class": "rule_515007",
            "checkpoint_amount": 2,
        },
        107016: {
            "class": "rule_107016",
            "checkpoint_amount": 3,
        },
        103074: {
            "class": "rule_103074",
            "checkpoint_amount": 1,
        },
        106020: {
            "class": "rule_106020",
            "checkpoint_amount": 1,
        },
        106029: {
            "class": "rule_106029",
            "checkpoint_amount": 5,
        },
        106030: {
            "class": "rule_106030",
            "checkpoint_amount": 2,
        },
        105018: {
            "class": "rule_105018",
            "checkpoint_amount": 1,
        },
        106028: {
            "class": "rule_106028",
            "checkpoint_amount": 5,
        },
        107012: {
            "class": "rule_107012",
            "checkpoint_amount": 2,
        },
        103064: {
            "class": "rule_103064",
            "checkpoint_amount": 1,
        },
        104047: {
            "class": "rule_104047",
            "checkpoint_amount": 2,
        },
        104052: {
            "class": "rule_104052",
            "checkpoint_amount": 2,
        },
        106017: {
            "class": "rule_106017",
            "checkpoint_amount": 2,
        },
        107009: {
            "class": "rule_107009",
            "checkpoint_amount": 3,
        },
        108006: {
            "class": "rule_108006",
            "checkpoint_amount": 1,
        },
        108008: {
            "class": "rule_108008",
            "checkpoint_amount": 2,
        },
        108010: {
            "class": "rule_108010",
            "checkpoint_amount": 1,
        },
        103079: {
            "class": "rule_103079",
            "checkpoint_amount": 1,
        },
        103062: {
            "class": "rule_103062",
            "checkpoint_amount": 1,
        },
        104050: {
            "class": "rule_104050",
            "checkpoint_amount": 1,
        },
        105019: {
            "class": "rule_105019",
            "checkpoint_amount": 2,
        },
    }


class CargoCheckRuleEngine:
    RULE_PATH = "rule_engine.rules."
    SPECIAL_BORDER_RULE_PATH = RULE_PATH + "cargo_check_rule.{module}"
    RULE_CLASS_NAME = "Rule"

    """
    "规则ID": {
        "major": "专业"
        "pack": "包名",
        "module": "文件名",
        "class_name": "规则类名",
        "checkpoint_amount": 2
    }
    """
    RULE = {
        # 建筑单图框
        # "1103xxx": {
        #     "major": "architecture",
        #     "pack": "BGY",
        #     "module": "rule_1103xxx",
        #     "class_name": "Rule",
        #     "checkpoint_amount": 1,
        # },
        "1103001": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103001",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1103002": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103002",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1103003": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103003",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1103004": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103004",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1103005": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103005",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1103006": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103006",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1103007": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103007",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1103008": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103008",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1103009": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103009",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1103010": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103010",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1103011": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103011",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1103015": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103015",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1103016": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103016",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1103017": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103017",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1103021": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103021",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1103012": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103012",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1303001": {
            "major": "plumbing",
            "pack": "BGY",
            "module": "rule_1303001",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1303003": {
            "major": "plumbing",
            "pack": "BGY",
            "module": "rule_1303003",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1303005": {
            "major": "plumbing",
            "pack": "BGY",
            "module": "rule_1303005",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1103014": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103014",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1103019": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103019",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1103020": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103020",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1103022": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103022",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1103024": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103024",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1103025": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103025",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1103026": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103026",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1103028": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1103028",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1103029": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103029",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1103031": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103031",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1103032": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103032",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1103033": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103033",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1103034": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103034",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1103035": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103035",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1103036": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103036",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1103039": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103039",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1103040": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103040",
            "class_name": "Rule",
            "checkpoint_amount": 3,
        },
        "1103041": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103041",
            "class_name": "Rule",
            "checkpoint_amount": 4,
        },
        "1103042": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103042",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1103045": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103045",
            "class_name": "Rule",
            "checkpoint_amount": 2
        },
        "1103047": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103047",
            "class_name": "Rule",
            "checkpoint_amount": 4
        },
        "1103048": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103048",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },

        "1303002": {
            "major": "plumbing",
            "pack": "BGY",
            "module": "rule_1303002",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1303004": {
            "major": "plumbing",
            "pack": "BGY",
            "module": "rule_1303004",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1103027": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103027",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1103037": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103037",
            "class_name": "Rule",
            "checkpoint_amount": 5,
        },
        "1103013": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103013",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1103018": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103018",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1103023": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103023",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1103030": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103030",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1103038": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103038",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1203001": {
            "major": "structure",
            "pack": "BGY",
            "module": "rule_1203001",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1203002": {
            "major": "structure",
            "pack": "BGY",
            "module": "rule_1203002",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1203003": {
            "major": "structure",
            "pack": "BGY",
            "module": "rule_1203003",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1203004": {
            "major": "structure",
            "pack": "BGY",
            "module": "rule_1203004",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1603012": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603012",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1603017": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603017",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },

        "1603020": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603020",
            "class_name": "Rule",
            "checkpoint_amount": 3,
        },

        "1603014": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603014",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1603021": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603021",
            "class_name": "Rule",
            "checkpoint_amount": 3,
        },
        "1603019": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603019",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        # 装修阶段规则
        "1603022": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603022",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1103046": {
            "major": "architecture",
            "pack": "BGY",
            "module": "rule_1103046",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1603002": {
            "major": "decor_electric",
            "pack": "BGY",
            "module": "rule_1603002",
            "class_name": "Rule",
            "checkpoint_amount": 3,
        },
        "1603004": {
            "major": "decor_electric",
            "pack": "BGY",
            "module": "rule_1603004",
            "class_name": "Rule",
            "checkpoint_amount": 4,
        },
        "1103044": {
            "major": "deepen_aluminum_door_window",
            "pack": "BGY",
            "module": "rule_1103044",
            "class_name": "Rule",
            "checkpoint_amount": 3,
        },
        "1603013": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603013",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1603015": {
            "major": "decor_hvac",
            "pack": "BGY",
            "module": "rule_1603015",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1603016": {
            "major": "decor_electric",
            "pack": "BGY",
            "module": "rule_1603016",
            "class_name": "Rule",
            "checkpoint_amount": 4,
        },
        "1603018": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603018",
            "class_name": "Rule",
            "checkpoint_amount": 6,
        },
        "1603094": {
            "major": "decor_electric",
            "pack": "BGY",
            "module": "rule_1603094",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1603001": {
            "major": "decor_electric",
            "pack": "BGY",
            "module": "rule_1603001",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1603003": {
            "major": "decor_electric",
            "pack": "BGY",
            "module": "rule_1603003",
            "class_name": "Rule",
            "checkpoint_amount": 3,
        },
        "1603005": {
            "major": "decor_electric",
            "pack": "BGY",
            "module": "rule_1603005",
            "class_name": "Rule",
            "checkpoint_amount": 4,
        },
        "1603006": {
            "major": "decor_electric",
            "pack": "BGY",
            "module": "rule_1603006",
            "class_name": "Rule",
            "checkpoint_amount": 4,
        },
        "1603007": {
            "major": "decor_plumbing",
            "pack": "BGY",
            "module": "rule_1603007",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1603008": {
            "major": "decor_plumbing",
            "pack": "BGY",
            "module": "rule_1603008",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1603009": {
            "major": "decor_plumbing",
            "pack": "BGY",
            "module": "rule_1603009",
            "class_name": "Rule",
            "checkpoint_amount": 3,
        },
        "1603010": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603010",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1603011": {
            "major": "decor_electric",
            "pack": "BGY",
            "module": "rule_1603011",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1603043": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603043",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1603044": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603044",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1603045": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603045",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1603046": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603046",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1603023": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603023",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1603027": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603027",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1603030": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603030",
            "class_name": "Rule",
            "checkpoint_amount": 4,
        },
        "1603033": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603033",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1603034": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603034",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1603039": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603039",
            "class_name": "Rule",
            "checkpoint_amount": 9,
        },
        "1603040": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603040",
            "class_name": "Rule",
            "checkpoint_amount": 10,
        },
        "1603041": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603041",
            "class_name": "Rule",
            "checkpoint_amount": 10,
        },
        "1603042": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603042",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1603047": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603047",
            "class_name": "Rule",
            "checkpoint_amount": 6,
        },
        "1603048": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603048",
            "class_name": "Rule",
            "checkpoint_amount": 6,
        },
        "1603049": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603049",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1603052": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603052",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1603053": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603053",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1603054": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603054",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1603055": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603055",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1603056": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603056",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1603057": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603057",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1603058": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603058",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1603059": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603059",
            "class_name": "Rule",
            "checkpoint_amount": 8,
        },
        "1603060": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603060",
            "class_name": "Rule",
            "checkpoint_amount": 8,
        },
        "1603061": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603061",
            "class_name": "Rule",
            "checkpoint_amount": 8,
        },
        "1603062": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603062",
            "class_name": "Rule",
            "checkpoint_amount": 8,
        },
        "1603064": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603064",
            "class_name": "Rule",
            "checkpoint_amount": 8,
        },
        "1603065": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603065",
            "class_name": "Rule",
            "checkpoint_amount": 8,
        },
        "1603066": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603066",
            "class_name": "Rule",
            "checkpoint_amount": 8,
        },
        "1603067": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603067",
            "class_name": "Rule",
            "checkpoint_amount": 8,
        },
        "1603069": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603069",
            "class_name": "Rule",
            "checkpoint_amount": 8,
        },
        "1603070": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603070",
            "class_name": "Rule",
            "checkpoint_amount": 10,
        },
        "1603071": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603071",
            "class_name": "Rule",
            "checkpoint_amount": 10,
        },
        "1603072": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603072",
            "class_name": "Rule",
            "checkpoint_amount": 9,
        },
        "1603024": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603024",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1603025": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603025",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1603026": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603026",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1603028": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603028",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1603029": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603029",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1603031": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603031",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1603032": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603032",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1603035": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603035",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1603036": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603036",
            "class_name": "Rule",
            "checkpoint_amount": 3,
        },
        "1603037": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603037",
            "class_name": "Rule",
            "checkpoint_amount": 4,
        },
        "1603038": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603038",
            "class_name": "Rule",
            "checkpoint_amount": 3,
        },
        "1603050": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603050",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1603051": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603051",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        # "1603063": {
        #     "major": "decor_architecture",
        #     "pack": "BGY",
        #     "module": "rule_1603063",
        #     "class_name": "Rule",
        #     "checkpoint_amount": 1,
        # },
        "1603068": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603068",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1603074": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603074",
            "class_name": "Rule",
            "checkpoint_amount": 4,
        },
        "1603075": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603075",
            "class_name": "Rule",
            "checkpoint_amount": 3,
        },
        "1603076": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603076",
            "class_name": "Rule",
            "checkpoint_amount": 3,
        },
        "1603077": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603077",
            "class_name": "Rule",
            "checkpoint_amount": 4,
        },
        "1603078": {
            "major": "decor_hvac",
            "pack": "BGY",
            "module": "rule_1603078",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1603079": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603079",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1603080": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603080",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1603081": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603081",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1603082": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603082",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        # "1603083": {
        #     "major": "decor_architecture",
        #     "pack": "BGY",
        #     "module": "rule_1603083",
        #     "class_name": "Rule",
        #     "checkpoint_amount": 1,
        # },
        # "1603084": {
        #     "major": "decor_architecture",
        #     "pack": "BGY",
        #     "module": "rule_1603084",
        #     "class_name": "Rule",
        #     "checkpoint_amount": 1,
        # },
        "1603088": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603088",
            "class_name": "Rule",
            "checkpoint_amount": 2,
        },
        "1603089": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603089",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1603090": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603090",
            "class_name": "Rule",
            "checkpoint_amount": 3,
        },
        "1603091": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603091",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
        "1603092": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603092",
            "class_name": "Rule",
            "checkpoint_amount": 4,
        },
        "1603093": {
            "major": "decor_architecture",
            "pack": "BGY",
            "module": "rule_1603093",
            "class_name": "Rule",
            "checkpoint_amount": 1,
        },
    }


"""
    import importlib
    from config_manager.rule_engine import RuleEngineV2
    rule_file_name = RuleEngineV2.RULE[rule_id]["class"]
    rule_path = f"{RuleEngineV2.SINGLE_BORDER_RULE_PATH}.{rule_file_name}"
    rule_module = importlib.import_module(rule_path)
    rule = getattr(rule_module, RuleEngineV2.RULE_CLASS_NAME)(border_name, border_entity_info, rule_id)   # (图框名称，图框构件字典，结果保存路径，审查点总数）
    result = rule.run()
"""

# 规则筛选
cargo_milestone2_rule_list = ['1103001', '1103002', '1103003', '1103004', '1103005', '1103006', '1103007', '1103008',
                              '1103009', '1103010', '1103011', '1103012', '1103013', '1103014', '1103015', '1103016',
                              '1103017', '1103018', '1103019', '1103020', '1103021', '1103022', '1103023', '1103024',
                              '1103025', '1103026', '1103027', '1103028', '1103029', '1103030', '1103033', '1103034',
                              '1103035', '1103036', '1103037', '1103038', '1103039', '1103040', '1103042', '1103044',
                              '1103045', '1103046', '1103047', '1103048', '1203001', '1203002', '1203003', '1203004',
                              '1303001', '1303002', '1303003', '1303004', '1303005', '1603001', '1603002', '1603003',
                              '1603004', '1603005', '1603006', '1603010', '1603011', '1603013', '1603014', '1603015',
                              '1603016', '1603017', '1603018', '1603019', '1603020', '1603023', '1603024', '1603026',
                              '1603027', '1603028', '1603030', '1603031', '1603032', '1603033', '1603034', '1603035',
                              '1603036', '1603037', '1603038', '1603039', '1603040', '1603041', '1603042', '1603043',
                              '1603044', '1603045', '1603046', '1603047', '1603048', '1603049', '1603052', '1603053',
                              '1603054', '1603055', '1603056', '1603057', '1603058', '1603059', '1603060', '1603061',
                              '1603064', '1603065', '1603066', '1603069', '1603070', '1603071', '1603074', '1603075',
                              '1603076', '1603079', '1603080', '1603081', '1603082', '1603090', '1603092', '1603094']

for i in list(CargoCheckRuleEngine.RULE.keys()):
    if i not in cargo_milestone2_rule_list:
        CargoCheckRuleEngine.RULE.pop(i)
