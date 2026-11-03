# 16. 테스트(unittest)

코드를 고칠 때마다 손으로 하나하나 실행해 확인하기는 어렵습니다. **테스트 코드**를 써 두면 명령 한 번으로 "예전처럼 잘 동작하는지"를 자동으로 확인할 수 있습니다.

## unittest 기본 구조

```python
import unittest

class 무엇을_테스트하는지(unittest.TestCase):   # TestCase 를 상속
    def test_어떤_경우(self):                  # 이름이 test 로 시작하는 메서드가 하나의 테스트
        self.assertEqual(실제값, 기대값)
```

| 검사 메서드 | 통과 조건 |
|---|---|
| `assertEqual(a, b)` | `a == b` |
| `assertTrue(x)` / `assertFalse(x)` | 참 / 거짓 |
| `assertIn(a, b)` | `a in b` |
| `assertIsNone(x)` | `x is None` |
| `assertAlmostEqual(a, b)` | 실수가 거의 같음 (`0.1 + 0.2` 같은 오차 허용) |
| `with assertRaises(Error):` | 블록 안에서 그 예외가 발생 |

## 실행해 보기

테스트 대상:

```python title="examples/ch16_testing/calc_utils.py"
--8<-- "examples/ch16_testing/calc_utils.py"
```

테스트 코드:

```python title="examples/ch16_testing/test_calc_utils.py"
--8<-- "examples/ch16_testing/test_calc_utils.py"
```

```powershell
cd examples\ch16_testing
python -m unittest -v
```

```text
test_empty_raises (test_calc_utils.AverageTest.test_empty_raises) ... ok
test_float (test_calc_utils.AverageTest.test_float) ... ok
...
Ran 5 tests in 0.001s

OK
```

하나라도 실패하면 `FAILED (failures=1)`과 함께 **무엇을 기대했고 실제로는 무엇이 나왔는지** 보여 줍니다.

## 테스트 찾기 규칙 (discover)

`python -m unittest`는 **현재 폴더**에서 `test*.py` 파일을 찾아 실행합니다. 테스트가 `tests` 폴더에 모여 있다면:

```powershell
python -m unittest discover -s tests -v
```

이 위키 저장소도 같은 방식으로 **모든 예제가 실제로 실행되는지** 검사합니다. `tests/test_examples.py`를 열어 보세요. `subprocess`로 예제를 실행하고 출력에 기대한 문장이 있는지 확인합니다.

## 좋은 테스트를 쓰는 요령

- **정상 경우 + 경계 경우 + 오류 경우**를 함께 씁니다. (예: 보통 리스트, 빈 리스트, 잘못된 입력)
- 테스트 하나는 **한 가지**만 확인하고, 이름으로 무엇을 확인하는지 드러냅니다.
- 네트워크·메일 발송·현재 시각처럼 **매번 결과가 달라지는 것**은 테스트에서 직접 쓰지 않습니다. 샘플 파일을 읽게 하거나, 로컬 서버를 띄우거나, `unittest.mock`으로 가짜 객체를 씁니다.
- 테스트가 만드는 파일은 `tempfile.TemporaryDirectory()` 같은 임시 폴더에 둡니다.
- 버그를 고칠 때는 **그 버그를 재현하는 테스트를 먼저** 쓰고, 고친 뒤 통과하는지 확인합니다.

## unittest.mock 맛보기

```python
import unittest
from unittest import mock

def get_status(session, url):
    return session.get(url, timeout=10).status_code

class GetStatusTest(unittest.TestCase):
    def test_uses_timeout(self):
        fake = mock.Mock()
        fake.get.return_value.status_code = 200
        self.assertEqual(get_status(fake, "https://example.com"), 200)
        fake.get.assert_called_once_with("https://example.com", timeout=10)

unittest.main(argv=["x"], exit=False)
```

실제 네트워크 없이 "timeout 을 넘겼는지"까지 확인할 수 있습니다.

## 연습문제

1. `calc_utils.py`에 `clamp(value, low, high)`(범위를 벗어나면 끝 값으로 맞추기)를 추가하고, 범위 안·아래·위 세 경우의 테스트를 쓰세요.
2. 일부러 `average`를 틀리게 고쳐(`len(numbers) + 1`로 나누기) 테스트가 실패하는 모습을 확인한 뒤 되돌리세요.

??? success "해답"
    ```python
    import unittest

    def clamp(value, low, high):
        return max(low, min(value, high))

    class ClampTest(unittest.TestCase):
        def test_inside(self):
            self.assertEqual(clamp(5, 0, 10), 5)

        def test_below(self):
            self.assertEqual(clamp(-3, 0, 10), 0)

        def test_above(self):
            self.assertEqual(clamp(99, 0, 10), 10)

    unittest.main(argv=["x"], exit=False)
    ```
    2번: `AssertionError: 1.5 != 2`처럼 기대값과 실제값이 표시됩니다.
