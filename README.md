### docker_stats_log.py
เก็บผล resource จาก docker stats สร้างเป็น csv file

#### Requirement
[docker](https://pypi.org/project/docker/)

[hurry.filesize](https://pypi.org/project/hurry.filesize/)

หรือใช้คำสั่ง 
`pip install docker hurry.filesize`

#### Usage

  1. แก้ container_name หรือ config ในไฟล์ docker_stats_log.py
        
        e.g.

        ```
        config = {
                'env': "zeta",
                'action': "recal"
            }
        resource_report(container_name='dailka', config=config)

        or set filename

        resource_report(container_name='dailka', config=config,filename='data.csv')
        ```

  2. Run project ต่างๆ เช่น dailka ด้วย docker-compose  
  3. เปิด project นี้แล้ว run `python docker_stats_log.py`

#### CSV example

default name: resource_result.csv

| ENV  | Action | Memory_limit (MiB) | Date       | Time     | CPU_percentage | Memory_usage (MiB) | Memory_percentage |
| ---- | ------ | ------------------ | ---------- | -------- | -------------- | ------------------ | ----------------- |
| zeta | recal  | 1000               | 2021-09-02 | 17:00:34 | 156.25         | 143                | 14.38             |
| zeta | recal  | 1000               | 2021-09-02 | 17:00:36 | 185.66         | 241                | 24.17             |
| zeta | recal  | 1000               | 2021-09-02 | 17:00:38 | 7.02           | 272                | 27.29             |

