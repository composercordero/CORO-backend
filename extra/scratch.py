programs = [
  {
      "hymn": {
          "Arranger:": 'null',
          "Audio recording:": "https://hymnary.org/media/fetch/150502/hymnary/audio/GG2013/725-OJesusIHave_accomp.mp3",
          "Author:": "John Ernest Bode",
          "Copyright:": "Adapt. and Harm.© 1927 Oxford University Press",
          "First Line:": "O Jesus, I have promised",
          "Hymnal Number:": "725",
          "Key:": "E♭ Major",
          "Language:": "English",
          "Meter:": "7.6.7.6.D",
          "Publication Date:": "2013",
          "Source:": "Finnish folk melody",
          "Title:": "O Jesus, I Have Promised",
          "Tune Name:": "NYLAND",
          "id": 2
      },
      "id": 2,
      "service": {
          "Service Date:": "2023-01-08",
          "id": 1
      }
  },
  {
      "hymn": {
          "Arranger:": 'null',
          "Audio recording:": "https://hymnary.org/media/fetch/149230/hymnary/audio/GG2013/720%20jesus%20calls%20us.mp3",
          "Author:": "Cecil Frances Alexander",
          "Copyright:": 'null',
          "First Line:": "Jesus calls us; o'er the tumult",
          "Hymnal Number:": "720",
          "Key:": "A♭ Major",
          "Language:": "English",
          "Meter:": "8.7.8.7",
          "Publication Date:": "2013",
          "Source:": 'null',
          "Title:": "Jesus Calls Us",
          "Tune Name:": "GALILEE",
          "id": 3
      },
      "id": 3,
      "service": {
          "Service Date:": "2023-01-08",
          "id": 1
      }
  }
]

for p in programs:
    print(p['hymn']['Hymnal Number:'])
    print('-------')