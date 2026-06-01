import re

class TextParser:
    def split_sentences(self, text):
        # 按照句号、感叹号、问号、换行切分
        sentences = re.split(r'([。！？\n])', text)
        result = []
        for i in range(0, len(sentences) - 1, 2):
            s = sentences[i].strip() + sentences[i+1].strip()
            if s.strip():
                result.append(s.strip())
        # 处理最末尾没有标点的情况
        if len(sentences) % 2 == 1 and sentences[-1].strip():
            result.append(sentences[-1].strip())
        return [r for r in result if r]
        
    def parse(self, text, is_bilingual=False):
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        pairs = []
        if is_bilingual:
            for line in lines:
                if '|' in line:
                    zh, ko = line.split('|', 1)
                    pairs.append((zh.strip(), ko.strip()))
            return pairs
        return []
