def main():
    dict1 = {"hi": "not changed"}
    dict2 = {**dict1}
    dict2["hi2"] = "i added something"
    print(dict1)
    print(dict2)


if __name__ == "__main__":
    main()
