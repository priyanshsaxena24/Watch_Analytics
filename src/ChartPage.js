import React, { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import 'chart.js/auto';
import './ChartPage.css';

const processData = (data) => {
  const totalWatchTime = {};
  const mostViewedChannel = {};
  const mostViewedCategory = {};

  for (const day in data) {
    if (data[day].length === 0) {
      totalWatchTime[day] = null;
      mostViewedChannel[day] = null;
      mostViewedCategory[day] = null;
    } else {
      totalWatchTime[day] = 0;
      mostViewedChannel[day] = {};
      mostViewedCategory[day] = {};

      data[day].forEach(video => {
        totalWatchTime[day] += video.watchTime;

        if (mostViewedChannel[day][video.channelName]) {
          mostViewedChannel[day][video.channelName] += video.watchTime;
        } else {
          mostViewedChannel[day][video.channelName] = video.watchTime;
        }

        if (mostViewedCategory[day][video.category]) {
          mostViewedCategory[day][video.category] += video.watchTime;
        } else {
          mostViewedCategory[day][video.category] = video.watchTime;
        }
      });
    }
  }

  return { totalWatchTime, mostViewedChannel, mostViewedCategory };
};

const ChartPage = ({ data }) => {
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    const { totalWatchTime, mostViewedChannel, mostViewedCategory } = processData(data);

    const labels = Object.keys(data);
    const totalWatchTimeData = labels.map(day => totalWatchTime[day] !== null ? totalWatchTime[day] : 0);

    const findMaxKey = (obj) => {
      return obj ? Object.keys(obj).reduce((a, b) => (obj[a] > obj[b] ? a : b)) : null;
    };

    const mostViewedChannelData = labels.map(day => {
      const channel = findMaxKey(mostViewedChannel[day]);
      return channel ? { day, channel, watchTime: mostViewedChannel[day][channel] } : { day, channel: 'No Data', watchTime: 0 };
    });

    const mostViewedCategoryData = labels.map(day => {
      const category = findMaxKey(mostViewedCategory[day]);
      return category ? { day, category, watchTime: mostViewedCategory[day][category] } : { day, category: 'No Data', watchTime: 0 };
    });

    setChartData({
      labels,
      totalWatchTimeData,
      mostViewedChannelData,
      mostViewedCategoryData
    });
  }, [data]); 

  if (!chartData) return <div>Loading...</div>;

  return (
    <div>
      <h1>YouTube Watch Analytics</h1>
      
      <h2>Total Watch Time (Day/Date Wise)</h2>
      <Bar 
        data={{
          labels: chartData.labels,
          datasets: [{
            label: 'Total Watch Time (seconds)',
            data: chartData.totalWatchTimeData,
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
          }]
        }}
        options={{
          scales: {
            x: {
              grid: {
                display: false 
              }
            },
            y: {
              type : 'logarithmic',
              display: false, 
              beginAtZero: true
            }
          },
          plugins: {
            tooltip: {
              callbacks: {
                label: function(context) {
                  return `${context.raw} seconds`;
                }
              }
            },
            legend: {
              display: false
            }
          }
        }}
      />
      
      <h2>Most Viewed Channel (Day/Date Wise)</h2>
      <Bar 
        data={{
          labels: chartData.labels,
          datasets: [{
            label: 'Most Viewed Channel',
            data: chartData.mostViewedChannelData.map(item => item.watchTime),
            backgroundColor: 'rgba(153, 102, 255, 0.2)',
            borderColor: 'rgba(153, 102, 255, 1)',
            borderWidth: 1
          }]
        }}
        options={{
          scales: {
            x: {
              grid: {
                display: false 
              }
            },
            y: {
              type : 'logarithmic',
              display: false, 
              beginAtZero: true
            },
          },
          plugins: {
            tooltip: {
              callbacks: {
                label: function(context) {
                  const item = chartData.mostViewedChannelData[context.dataIndex];
                  return `${item.channel}: ${context.raw} seconds`;
                }
              }
            },
            legend: {
              display: false // Hide the legend
            }
          }
        }}
      />
      
      <h2>Most Viewed Category (Day/Date Wise)</h2>
      <Bar 
        data={{
          labels: chartData.labels,
          datasets: [{
            label: 'Most Viewed Category',
            data: chartData.mostViewedCategoryData.map(item => item.watchTime),
            backgroundColor: 'rgba(255, 159, 64, 0.2)',
            borderColor: 'rgba(255, 159, 64, 1)',
            borderWidth: 1
          }]
        }}
        options={{
          scales: {
            x: {
              grid: {
                display: false 
              }
            },
            y: {
              type : 'logarithmic',
              display: false, 
              beginAtZero: true
            }
          },
          plugins: {
            tooltip: {
              callbacks: {
                label: function(context) {
                  const item = chartData.mostViewedCategoryData[context.dataIndex];
                  return `${item.category}: ${context.raw} seconds`;
                }
              }
            },
            legend: {
              display: false
            }
          }
        }}
      />
    </div>
  );
};

export default ChartPage;
