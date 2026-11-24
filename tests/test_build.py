import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import build  # noqa: E402

HEAD = "<p>Özet.</p>"
TAIL = ("<p><em>AI açıklaması.</em></p>"
        '<p>Bölüm sayfası ve kaynaklar: <a href="https://x/bolum/d/">https://x/bolum/d/</a></p>')


def notes(n):
    md = "### Öne çıkanlar\n\n" + "\n\n".join(f"**Haber {i}.** " + "uzun cümle " * 40 for i in range(n))
    md += "\n\n### Diğer gelişmeler\n\n" + "\n".join(f"- Kısa haber {i} " + "x" * 200 for i in range(n))
    return build.md_to_html(md)


class FitDescription(unittest.TestCase):
    def test_short_episode_unchanged(self):
        short = notes(1)
        self.assertEqual(build.fit_description(HEAD, short, TAIL), HEAD + short + TAIL)

    def test_oversized_episode_is_capped_and_keeps_tail(self):
        long = notes(30)
        self.assertGreater(len(HEAD + long + TAIL), build.DESCRIPTION_CAP)
        out = build.fit_description(HEAD, long, TAIL)
        self.assertLessEqual(len(out), build.DESCRIPTION_CAP)
        self.assertTrue(out.startswith(HEAD))
        self.assertTrue(out.endswith(build.NOTES_DROPPED + TAIL))
        body = out[len(HEAD):-len(build.NOTES_DROPPED + TAIL)]
        self.assertTrue(body)
        self.assertTrue(set(body.splitlines()) <= set(long.splitlines()))  # whole blocks only
        self.assertEqual(body.count("<ul>"), body.count("</ul>"))

    def test_cut_inside_list_closes_it(self):
        md = "### Diğer\n\n" + "\n".join(f"- madde {i} " + "y" * 300 for i in range(40))
        out = build.fit_description(HEAD, build.md_to_html(md), TAIL)
        self.assertLessEqual(len(out), build.DESCRIPTION_CAP)
        self.assertIn("</ul>" + build.NOTES_DROPPED, out)

    def test_cap_holds_at_every_offset(self):
        # list-only notes: the cut lands inside the list, so the closing </ul> is budgeted
        long = build.md_to_html("### D\n\n" + "\n".join(f"- m {i} " + "y" * 97 for i in range(80)))
        for pad in range(0, 300):
            head = "<p>" + "s" * pad + "</p>"
            self.assertLessEqual(len(build.fit_description(head, long, TAIL)), build.DESCRIPTION_CAP, pad)

    def test_real_feed_items_fit(self):
        show, episodes = build.load()
        for ep in episodes:
            out = build.fit_description("<p>s</p>", build.notes_html(ep), TAIL)
            self.assertLessEqual(len(out), build.DESCRIPTION_CAP, ep["date"])


if __name__ == "__main__":
    unittest.main()
