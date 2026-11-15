/**
 * CornLearn LMS - Admin Analytics Dashboard Script
 * File: static/js/dashboard.js
 * Aligned with Stitch Academic Precision Design System
 */

(function () {
    "use strict";

    document.addEventListener("DOMContentLoaded", function () {
        initGenderRatioChart();
    });

    /**
     * Initializes the Student Gender Ratio Doughnut Chart on #genderRatioChart
     */
    function initGenderRatioChart() {
        const canvas = document.getElementById("genderRatioChart");
        if (!canvas) {
            return;
        }

        if (typeof Chart === "undefined") {
            console.warn("[CornLearn] Chart.js chưa được tải. Không thể hiển thị biểu đồ tỷ lệ giới tính.");
            return;
        }

        const males = parseFloat(canvas.dataset.males || canvas.getAttribute("data-males")) || 0;
        const females = parseFloat(canvas.dataset.females || canvas.getAttribute("data-females")) || 0;
        const total = males + females;

        const ctx = canvas.getContext("2d");

        // Fallback when both are 0 so the doughnut still renders cleanly at 0 students
        if (males === 0 && females === 0) {
            new Chart(ctx, {
                type: "doughnut",
                data: {
                    labels: ["Chưa có dữ liệu sinh viên"],
                    datasets: [
                        {
                            data: [1],
                            backgroundColor: ["#E2E8F0"],
                            hoverBackgroundColor: ["#CBD5E1"],
                            borderWidth: 2,
                            borderColor: "#FFFFFF"
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: "70%",
                    plugins: {
                        legend: {
                            position: "bottom",
                            labels: {
                                font: {
                                    family: "'Be Vietnam Pro', sans-serif",
                                    size: 13,
                                    weight: "500"
                                },
                                color: "#42474F",
                                boxWidth: 12,
                                padding: 16,
                                usePointStyle: true
                            }
                        },
                        tooltip: {
                            backgroundColor: "#131B2E",
                            padding: 12,
                            cornerRadius: 8,
                            callbacks: {
                                label: function () {
                                    return " Nam: 0% | Nữ: 0% (Chưa có dữ liệu)";
                                }
                            }
                        }
                    }
                }
            });
            return;
        }

        const malePct = total > 0 ? Math.round((males / total) * 1000) / 10 : males;
        const femalePct = total > 0 ? Math.round((females / total) * 1000) / 10 : females;

        new Chart(ctx, {
            type: "doughnut",
            data: {
                labels: ["Nam", "Nữ"],
                datasets: [
                    {
                        label: "Tỷ lệ Giới tính Sinh viên",
                        data: [males, females],
                        backgroundColor: [
                            "#164E80", // Institutional Navy (Nam)
                            "#2563EB"  // Royal Blue CTA (Nữ)
                        ],
                        hoverBackgroundColor: [
                            "#003761",
                            "#1D4ED8"
                        ],
                        borderWidth: 2,
                        borderColor: "#FFFFFF",
                        hoverOffset: 6
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: "70%",
                layout: {
                    padding: {
                        top: 8,
                        bottom: 8
                    }
                },
                plugins: {
                    legend: {
                        position: "bottom",
                        labels: {
                            font: {
                                family: "'Be Vietnam Pro', sans-serif",
                                size: 13,
                                weight: "500"
                            },
                            color: "#131B2E",
                            padding: 16,
                            boxWidth: 12,
                            usePointStyle: true
                        }
                    },
                    tooltip: {
                        backgroundColor: "#131B2E",
                        titleFont: {
                            family: "'Be Vietnam Pro', sans-serif",
                            size: 13,
                            weight: "600"
                        },
                        bodyFont: {
                            family: "'Be Vietnam Pro', sans-serif",
                            size: 12
                        },
                        padding: 12,
                        cornerRadius: 8,
                        boxPadding: 4,
                        callbacks: {
                            title: function () {
                                return "Tỷ lệ Giới tính Sinh viên";
                            },
                            label: function (context) {
                                const isMale = context.dataIndex === 0;
                                const labelName = isMale ? "Nam" : "Nữ";
                                const pct = isMale ? malePct : femalePct;
                                return ` ${labelName}: ${pct}%`;
                            }
                        }
                    }
                }
            }
        });
    }
})();
