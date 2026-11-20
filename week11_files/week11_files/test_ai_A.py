# pytest tests (run with: pytest load_scores.py)
def test_load_scores_valid_rows_and_duplicate_names(tmp_path):
    path = tmp_path / "scores.csv"
    path.write_text("이름,점수\n민수,80\n민수,90\n", encoding="utf-8")

    assert load_scores(path) == ([('민수', 80), ('민수', 90)], [])


def test_load_scores_header_only_and_empty_file(tmp_path):
    header = tmp_path / "header.csv"
    header.write_text("이름,점수\n", encoding="utf-8")
    empty = tmp_path / "empty.csv"
    empty.write_text("", encoding="utf-8")

    assert load_scores(header) == ([], [])
    assert load_scores(empty) == ([], [])


def test_load_scores_missing_file_raises(tmp_path):
    import pytest

    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


def test_load_scores_score_boundaries_and_whitespace(tmp_path):
    path = tmp_path / "boundaries.csv"
    path.write_text("이름,점수\n최저,0\n최고,100\n 공백 , 50 \n", encoding="utf-8")

    assert load_scores(path) == ([('최저', 0), ('최고', 100), ('공백', 50)], [])


def test_load_scores_skips_invalid_rows_with_reasons_and_line_numbers(tmp_path):
    path = tmp_path / "invalid.csv"
    path.write_text(
        "이름,점수\n"
        "열 하나\n"
        "가,1,추가\n"
        ",80\n"
        "나,\n"
        "다,abc\n"
        "라,-1\n"
        "마,101\n"
        "\n"
        "바,70\n",
        encoding="utf-8",
    )

    kept, skipped = load_scores(path)

    assert kept == [('바', 70)]
    assert skipped == [
        (2, "열 하나", "열 개수가 2가 아님"),
        (3, "가,1,추가", "열 개수가 2가 아님"),
        (4, ",80", "이름이 비어 있음"),
        (5, "나,", "점수가 비어 있음"),
        (6, "다,abc", "점수가 정수가 아님"),
        (7, "라,-1", "점수가 0~100 밖"),
        (8, "마,101", "점수가 0~100 밖"),
    ]
