from pathlib import Path
from typing import List

dir = Path(__file__).parent.resolve()

def main():
	public_dir = Path(f"{dir}/../docs")
	files = searching_all_files(public_dir)
	
	links = [f"[{f}](/{f})" for f in files]
	with open(f"{dir}/../docs/index.md", "w") as file:
		file.write("\n".join(links))


def searching_all_files(directory: Path)-> List[str]:   
	file_list = []

	for x in directory.iterdir():
		if x.is_file():
			if x.name == "index.md":
				continue
			file_list.append(x.name)

	return file_list

if __name__ == "__main__":
	main()