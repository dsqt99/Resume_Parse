# Run with Dockerfile
```
docker build -t cv_extract .
docker run -p 8080:8080 --network=host cv_extract:latest
```

- Result will be saved in results.json with format:
```
{
    "avatar_path": "http://localhost:1202/502be82c-326f-4465-bf0d-bdd82cf5fa44.png",
    "infos": {
        "full_name": "TRỊNH VĂN HIẾU",
        "position": "",
        "tel": "",
        "date_of_birth": "",
        "email": "",
        "gender": "",
        "address": "CC ài Hạn muốn trở thành CTO hoặc PM tại nơi làm việc",
        "work_experience": [
            {
                "company": "",
                "position": "",
                "description": "",
                "from": "",
                "to": ""
            }
        ],
        "study": [
            {
                "uni": "",
                "specialized": "",
                "degree": "",
                "description": "",
                "graduation_type": "",
                "from": "",
                "to": ""
            }
        ],
        "career_goals": " Ngắn hạn: ồn định lại công việc, đóng góp cống hiến kinh nghiệm công việc cho r việc Dài Hạn muốn trỏ thành CTO hoặc PM tại nơi làm việc",
        "level_learning": "Đại học",
        "skills": " PHP,MYSQL,PGSQL,JAVASCRIPT , HTML,HTML5,CSS..... Có 10 năm kinh nghiệm PHP FRAMEWORK: LARAVEL,CODEIGNITER, ZEND FRAMEWORK, YIl FRAMEWORK , CAKE PHP... Sử dụng thành thạo GIT, SVN, TRELLO, JIRA.. Thành Thạo.",
        "work_addr": "",
        "prizes": "",
        "certificates": "",
        "hobbies": " Chơi được các môn thể thao, tìm hiểu công nghệ mới, giao lưu kết bạn",
        "reference": "",
        "activities": "",
        "projects": "",
        "extra_info": "(& GAME ONLINE // 2019 - 2023 Khách hàng Công Ty Cổ Phần Giải Trí Tendo Số lượng người tham gia 2o Người Vị trí CTO, PGD Xây dựng hệ thống cho công ty, Phát Triển SDK (android, ios), Xây dựng website game, web dịch vụ(nap.id...) các dịch vụ Liên quan.. Công nghệ sử dụng PHP Mysal Cake PHP aws googole big query\n(& GAME ONLINE // 2018 - 2019 Khách hàng Công Ty Cổ Phần Funtap Số lượng người tham gia 10 Người Vị trí Team Lead -. Maintain Hệ thống công ty, Phát Triển SDK (android, ios), Xay dung website game, we dịch vụ(nap.id..) các dịch vụ liên quan.. Công nghệ sử dụng PHP Mysal Cake PHP.\n(& HTML5 // 2016 - 2016 Khách hàng Toppan Số lượng người tham gia 2o Người Vị trí TeamLead dev Content HTML5 Công nghệ sử dụng HTML5\n(& LIFECARD // 2015 - 2016 Khách hàng Toppan Số lượng người tham gia 2o Người Vị trí TeamLead Phát triển Server PHP Zend Framework Công nghệ sử dụng PHP MYSQL Zend Framework\nÊ CRMMỸ PHẨM // 2018 - 2023 Khách hàng Cá nhân (http:⁄⁄Levananh.com⁄) Số lượng người tham gia 1 Người Vị trí CTO, PGD Xây dựng website, CRM các tool cho khách hàng mỹ phẩm Công nghệ sử dụng\nLEAD // 2018 - 2020 Công Ty Cổ Phần Funtap Bảo trì và phát triển hệ thống core của công ty game funtap. Xây dựng các website game, api, tool mkt, phat trién sdk cho android va ios Được làm việc với data khách hàng lớn,sử dụng nhiều công nghệ trong công việc\n§' TSS-SOFTWARECOMVN // 2017 - 2018 Khach hang STARTUP Số lượng người tham gia 6 Người Vị trí CEO Phát triền hệ thống làm website nhanh bằng PHP Công nghệ sử dụng PHP Mysal Yii Framework\nàm ngay\ní- RPC - REMOTE PLAYER CONTROL // 2012 - 2013 Khách hàng khach hàng nhật bản Số lượng người tham gia 30 người Vị trí Developer php Code màn hình và API cho mobile app Công nghệ sử dụng PHP PostgreSQL\n© CEO // 2017 - 2018 Startup company tss-software.comvn Xây dựng hệ thống làm website nhanh Làm website cá nhân và công ty.\n(& MCR // 2014 - 2015 Khach hang MCR Số lượng người tham gia 10 Người Vị trí Dev và TeamLead Phát triển website theo yêu cầu khách hàng bằng PHP Công nghệ sử dụng PHP MYSQL Zend Framework\nšz BLOGG // 2013 - 2014 Khách hàng Khách hàng nhật bản Số lượng người tham gia 12 Người Vị trí Dev php -Deva blog for teen girl. Công nghệ sử dụng PHP MYSQL Smarty 2.x\nLINUX Cài đặt,sử dụng command line thành thạo TƯ DUY VÀ LOGIC Nghiên cứu và tìm kiếm giải quyết vấn đề nhanh và hiệu quả\nšz BLOGG // 2013 - 2014 Khách hàng Khách hàng nhật bản Số lượng người tham gia 12 Người Vị trí Dev php\n“AM. Ša . \"\":((d... @® 076907777 a @ Vinhome smartcity Tay Mo Nam Từ Liêm Hà Nội\n&› TECH LEAD, PGĐ... // 2020 - 2023 Công Ty Cổ Phần Giải Trí Tendo Làm hệ thống Server, website, sdk phục vụ công ty phát hành game"
    }
}
```