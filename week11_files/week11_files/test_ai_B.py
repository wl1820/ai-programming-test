def test_load_scores_whitespace_only_fields_and_blank_lines(tmp_path):
    path = tmp_path / "whitespace.csv"
    path.write_text("이름,점수\n   ,80\n가,   \n\n나,50\n", encoding="utf-8")

    kept, skipped = load_scores(path)

    assert kept == [("나", 50)]
    assert skipped == [
        (2, "   ,80", "이름이 비어 있음"),
        (3, "가,   ", "점수가 비어 있음"),
    ]