---
layout: default
datapoints: '[92.8366556334124, 94.87839844920984, 94.5789004094258, 96.03276857726675, 95.5875724896741]'
color: 'rgba(0, 118, 214, 1)'
background_color: 'rgba(232, 245, 255, 1)'
min: '0'
max: '100'
years: '[2021, 2022, 2023, 2024, 2025]'
title: 'Test Sparkline'
description: 'Test Description'
---

<div id="main-content" role="main" class="index-container">
  <section class="spending-trends-section bg-white">
    <div class="grid-container">
      <div class="grid-row">
        <div class="grid-col-12">
          <h3 class="spending-trends-header">Government-wide trends</h3>
        </div>
      </div>
      <ul class="usa-card-group grid-row spending-trends-cards">
        <li class="usa-card mobile:grid-col-12 tablet:grid-col-6 desktop:grid-col-4">
            {% include _sparklines-chart.html
            datapoints=page.datapoints
            color=page.color
            background_color=page.background_color
            min=page.min
            max=page.max
            years=page.years
            title=page.title
            caption=page.caption %}
        </li>
      </ul>
    </div>
  </section>
</div>