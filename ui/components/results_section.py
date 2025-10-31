"""
Results display with metrics, action buttons, and 5 tabs.
"""
import streamlit as st


def render_results_header():
    """Render success header"""
    st.markdown("---")
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #15803D 0%, #14532D 100%); 
                padding: 1.5rem; border-radius: 12px; text-align: center;'>
        <h2 style='color: white; margin: 0;'>🎉 Your Travel Plan is Ready!</h2>
        <p style='margin: 0.5rem 0 0 0; color: white; opacity: 0.95;'>
            Scroll down to explore your personalized itinerary
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)


def render_action_buttons():
    """Render quick action buttons"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.download_button(
            "📥 Download PDF",
            data="Sample PDF content",
            file_name="my_trip_plan.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    
    with col2:
        st.button("📧 Email Plan", use_container_width=True)
    
    with col3:
        st.button("🔄 Modify Plan", use_container_width=True)
    
    with col4:
        if st.button("🗑️ Clear Results", use_container_width=True):
            st.session_state.show_results = False
            st.session_state.generated_prompt = ""
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)


def count_total_activities(itinerary):
    """Helper to count total activities across all days"""
    total_activities = 0
    if isinstance(itinerary, list):
        for day in itinerary:
            if isinstance(day, dict):
                activities = day.get('activities', [])
                if isinstance(activities, list):
                    total_activities += len(activities)
    return total_activities


def render_trip_metrics(final_state):
    """Render key metrics cards"""
    st.markdown("### 📊 Trip Summary at a Glance")
    
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    final_plan = final_state.final_plan if hasattr(final_state, 'final_plan') else {}
    budget_summary = final_plan.get('budget_summary', {}) if isinstance(final_plan, dict) else {}
    
    with metric_col1:
        st.metric(
            label="Total Cost",
            value=f"${budget_summary.get('total_cost', 0)}",
            delta=f"-${budget_summary.get('savings', 0)}",
            delta_color="inverse"
        )
    
    with metric_col2:
        itinerary = final_plan.get('itinerary', []) if isinstance(final_plan, dict) else []
        itinerary_days = len(itinerary)
        st.metric(
            label="Duration",
            value=f"{itinerary_days} days" if itinerary_days > 0 else "TBD",
            delta="Perfect length"
        )
    
    with metric_col3:
        st.metric(
            label="Per Person",
            value=f"${budget_summary.get('per_person', 0)}",
            delta="Within budget"
        )
    
    with metric_col4:
        total_activities = count_total_activities(itinerary)
        st.metric(
            label="Activities",
            value=total_activities,
            delta="Planned"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)


def render_overview_tab(final_state):
    """Render Overview tab content"""
    st.markdown("### 🌟 Your Trip Overview")
    
    final_plan = final_state.final_plan if hasattr(final_state, 'final_plan') else {}
    trip_summary = final_plan.get('trip_summary', 
        "Experience the perfect blend of adventure and relaxation on this carefully curated journey.")
    
    st.markdown(f"""
    <div style='background-color: #FFFFFF; padding: 1.5rem; 
                border-radius: 8px; border-left: 4px solid #D97757; border: 1px solid #E7E5E4;'>
        <p style='font-size: 1.1rem; line-height: 1.7; margin: 0; color: #1C1917;'>
            {trip_summary}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Destination Research
    dest_research = final_state.destination_research if hasattr(final_state, 'destination_research') else {}
    
    if dest_research:
        st.markdown("### 🗺️ Suggested Destinations")
        
        suggested_destinations = dest_research.get('suggested_destinations', [])
        
        if suggested_destinations:
            for i, dest in enumerate(suggested_destinations, 1):
                if isinstance(dest, dict):
                    dest_name = dest.get('destination', f'Destination {i}')
                    dest_why = dest.get('why_suitable', '')
                    dest_attractions = dest.get('attractions', [])
                    dest_cost = dest.get('estimated_cost', 0)
                    
                    st.markdown(f"""
                    <div style='background-color: #FFFFFF; padding: 1.5rem; 
                                margin-bottom: 1rem; border-radius: 8px; 
                                border-left: 3px solid #D97757; border: 1px solid #E7E5E4;'>
                        <h4 style='margin: 0 0 0.5rem 0; color: #C8613D;'>
                            {i}. {dest_name}
                        </h4>
                        <p style='margin: 0.5rem 0; color: #1C1917;'>
                            {dest_why}
                        </p>
                        <p style='margin: 0.5rem 0 0 0; color: #44403C;'>
                            <strong>Top Attractions:</strong> {', '.join(dest_attractions) if dest_attractions else 'Various activities'}
                        </p>
                        <p style='margin: 0.5rem 0 0 0; color: #15803D; font-weight: 600;'>
                            Estimated Cost: ${dest_cost}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("Destination suggestions will be available soon")
    
    st.markdown("<br>", unsafe_allow_html=True)


def render_itinerary_tab(final_state):
    """Render Day-by-Day Itinerary tab"""
    st.markdown("### 📅 Your Day-by-Day Adventure")
    
    final_plan = final_state.final_plan if hasattr(final_state, 'final_plan') else {}
    itinerary = final_plan.get('itinerary', []) if isinstance(final_plan, dict) else []
    
    if not itinerary:
        st.info("No itinerary data available yet. The AI is still processing your request.")
    else:
        for idx, day_plan in enumerate(itinerary, start=1):
            if not isinstance(day_plan, dict):
                continue
            
            day_number = day_plan.get('day', idx)
            day_theme = day_plan.get('theme', 'Activities')
            day_cost = day_plan.get('total_day_cost', 0)
            
            with st.expander(
                f"**Day {day_number}:** {day_theme} (${day_cost})",
                expanded=(day_number == 1)
            ):
                activities = day_plan.get('activities', [])
                
                if not activities:
                    st.info("No activities planned for this day yet.")
                else:
                    for activity in activities:
                        if not isinstance(activity, dict):
                            continue
                        
                        activity_time = activity.get('time', 'TBD')
                        activity_name = activity.get('activity', 'Activity')
                        activity_location = activity.get('location', 'Location TBD')
                        activity_duration = activity.get('duration', 'TBD')
                        activity_cost = activity.get('estimated_cost', 0)
                        activity_notes = activity.get('notes', '')
                        
                        st.markdown(f"""
                        <div style='background-color: #FFFFFF; padding: 1rem; 
                                    margin-bottom: 1rem; border-radius: 8px; 
                                    border-left: 3px solid #D97757; border: 1px solid #E7E5E4;'>
                            <h4 style='margin: 0 0 0.5rem 0; color: #C8613D;'>
                                ⏰ {activity_time} - {activity_name}
                            </h4>
                            <p style='margin: 0.25rem 0; color: #1C1917;'>
                                <strong>📍 Location:</strong> {activity_location}<br>
                                <strong>⏱️ Duration:</strong> {activity_duration}<br>
                                <strong>💵 Cost:</strong> ${activity_cost}
                            </p>
                            {f"<p style='margin: 0.5rem 0 0 0; font-style: italic; color: #44403C;'>💡 {activity_notes}</p>" if activity_notes else ''}
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style='text-align: right; font-weight: 600; color: #15803D; 
                            padding-top: 0.5rem; border-top: 2px solid #E7E5E4;'>
                    Total Day Cost: ${day_cost}
                </div>
                """, unsafe_allow_html=True)


def render_budget_tab(final_state):
    """Render Budget Breakdown tab"""
    st.markdown("### 💰 Complete Budget Analysis")
    
    final_plan = final_state.final_plan if hasattr(final_state, 'final_plan') else {}
    budget_summary = final_plan.get('budget_summary', {}) if isinstance(final_plan, dict) else {}
    itinerary = final_plan.get('itinerary', []) if isinstance(final_plan, dict) else []
    
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Budget", f"${budget_summary.get('total_cost', 0)}")
    
    with col2:
        st.metric("Per Person", f"${budget_summary.get('per_person', 0)}")
    
    with col3:
        total_cost = budget_summary.get('total_cost', 0)
        num_days = len(itinerary)
        daily_avg = total_cost // num_days if num_days > 0 else 0
        st.metric("Daily Average", f"${daily_avg}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Budget breakdown
    breakdown = budget_summary.get('breakdown', {})
    
    if breakdown:
        st.markdown("#### 📊 Cost by Category")
        
        # Create visual breakdown
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Simple bar chart visualization
            import pandas as pd
            
            chart_data = pd.DataFrame({
                'Category': [cat.replace('_', ' ').title() for cat in breakdown.keys()],
                'Amount': list(breakdown.values())
            })
            
            st.bar_chart(chart_data, x='Category', y='Amount', height=300)
        
        with col2:
            st.markdown("**Detailed Breakdown:**")
            
            total = sum(breakdown.values())
            
            for category, amount in breakdown.items():
                percentage = (amount / total) * 100 if total > 0 else 0
                st.markdown(f"""
                <div style='margin-bottom: 1rem;'>
                    <strong style='color: #1C1917;'>{category.replace('_', ' ').title()}</strong><br>
                    <span style='font-size: 1.2rem; color: #D97757;'>${amount}</span>
                    <span style='color: #44403C;'> ({percentage:.1f}%)</span>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Budget breakdown will be available once the itinerary is complete.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Money-saving tips
    st.markdown("#### 💡 Money-Saving Tips")
    
    tips_col1, tips_col2 = st.columns(2)
    
    with tips_col1:
        st.markdown("""
        **Before You Go:**
        - ✓ Book flights 6-8 weeks in advance
        - ✓ Use price comparison tools
        - ✓ Consider shoulder season travel
        - ✓ Look for package deals
        """)
    
    with tips_col2:
        st.markdown("""
        **During Your Trip:**
        - ✓ Use public transportation
        - ✓ Eat at local restaurants
        - ✓ Book activities online in advance
        - ✓ Use city tourist cards
        """)


def render_essentials_tab(final_state):
    """Render Travel Essentials tab"""
    st.markdown("### ✈️ Essential Travel Information")
    
    final_plan = final_state.final_plan if hasattr(final_state, 'final_plan') else {}
    essentials = final_plan.get('travel_essentials', {}) if isinstance(final_plan, dict) else {}
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📋 Documentation")
        st.markdown(f"""
        **Visa Requirements:**  
        {essentials.get('visa', 'Check with embassy')}
        
        **Travel Insurance:**  
        {essentials.get('insurance', 'Recommended')}
        
        **Required Documents:**
        - Valid passport (6 months validity)
        - Return flight tickets
        - Hotel reservations
        - Travel insurance proof
        """)
        
        st.markdown("#### 💱 Money Matters")
        st.markdown(f"""
        **Currency:**  
        {essentials.get('currency', 'Local currency info')}
        
        **Payment Methods:**
        - Credit cards widely accepted
        - ATMs available throughout
        - Carry some cash for small vendors
        - Notify bank before traveling
        """)
    
    with col2:
        st.markdown("#### 🌡️ Weather & Climate")
        st.markdown(f"""
        **Expected Conditions:**  
        {essentials.get('weather', 'Check local forecast')}
        
        **What to Pack:**
        - Light layers for day
        - Warmer jacket for evenings
        - Comfortable walking shoes
        - Rain jacket (just in case)
        """)
        
        st.markdown("#### 🗣️ Communication")
        st.markdown(f"""
        **Language:**  
        {essentials.get('language', 'Local language info')}
        
        **Time Zone:**  
        {essentials.get('timezone', 'Local timezone')}
        
        **Useful Phrases:**
        - Hello / Thank you / Please
        - Download translation app
        - Learn basic numbers
        """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Health & Safety
    st.markdown("#### 🏥 Health & Safety")
    
    safety_col1, safety_col2 = st.columns(2)
    
    with safety_col1:
        st.markdown("""
        **Health Precautions:**
        - Check vaccination requirements
        - Pack basic first-aid kit
        - Bring prescription medications
        - Know emergency numbers (112)
        """)
    
    with safety_col2:
        st.markdown("""
        **Safety Tips:**
        - Register with embassy
        - Keep copies of documents
        - Be aware of surroundings
        - Use licensed taxis/rideshares
        """)


def render_packing_tab(final_state):
    """Render Packing List tab"""
    st.markdown("### 🎒 Smart Packing Checklist")
    
    final_plan = final_state.final_plan if hasattr(final_state, 'final_plan') else {}
    packing_list = final_plan.get('packing_list', []) if isinstance(final_plan, dict) else []
    
    if not packing_list:
        st.info("Packing list will be generated based on your destination and activities.")
    else:
        # Check if packing_list is a dictionary or list
        if isinstance(packing_list, dict):
            # Dictionary format
            pack_col1, pack_col2 = st.columns(2)
            
            categories = list(packing_list.keys())
            mid_point = len(categories) // 2
            
            with pack_col1:
                for category in categories[:mid_point + 1]:
                    st.markdown(f"#### {category}")
                    items = packing_list.get(category, [])
                    for i, item in enumerate(items):
                        st.checkbox(str(item), key=f"pack_{category}_{i}")
                    st.markdown("<br>", unsafe_allow_html=True)
            
            with pack_col2:
                for category in categories[mid_point + 1:]:
                    st.markdown(f"#### {category}")
                    items = packing_list.get(category, [])
                    for i, item in enumerate(items):
                        st.checkbox(str(item), key=f"pack_{category}_{i}")
                    st.markdown("<br>", unsafe_allow_html=True)
                    
        elif isinstance(packing_list, list):
            # List format
            st.markdown("#### Essential Items to Pack")
            
            pack_col1, pack_col2 = st.columns(2)
            mid_point = len(packing_list) // 2
            
            with pack_col1:
                for i, item in enumerate(packing_list[:mid_point]):
                    st.checkbox(str(item), key=f"pack_item_{i}")
            
            with pack_col2:
                for i, item in enumerate(packing_list[mid_point:], start=mid_point):
                    st.checkbox(str(item), key=f"pack_item_{i}")
        else:
            st.warning(f"Packing list format not recognized. Type: {type(packing_list)}")
    
    # Packing tips
    st.markdown("---")
    st.markdown("#### 💡 Pro Packing Tips")
    
    tips_col1, tips_col2, tips_col3 = st.columns(3)
    
    with tips_col1:
        st.markdown("""
        **Space Savers:**
        - Roll clothes instead of folding
        - Use packing cubes
        - Wear bulky items on plane
        """)
    
    with tips_col2:
        st.markdown("""
        **Smart Strategies:**
        - Pack versatile, mix-and-match items
        - Choose quick-dry fabrics
        - Leave room for souvenirs
        """)
    
    with tips_col3:
        st.markdown("""
        **Don't Forget:**
        - Check airline baggage limits
        - Weigh luggage before leaving
        - Keep valuables in carry-on
        """)


def render_feedback_section():
    """Render feedback and rating section"""
    st.markdown("### 🌟 Rate Your Experience")
    
    feedback_col1, feedback_col2 = st.columns([3, 1])
    
    with feedback_col1:
        rating = st.slider(
            "How satisfied are you with this travel plan?",
            1, 5, 3,
            format="%d ⭐",
            help="1 = Poor, 5 = Excellent"
        )
        
        feedback_text = st.text_area(
            "Additional comments (optional):",
            placeholder="What did you like? What could be improved?",
            height=100
        )
    
    with feedback_col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        if st.button("Submit Feedback", type="primary", use_container_width=True):
            st.success(f"Thank you for your {rating}-star rating! 🎉")
            st.balloons()
        
        if st.button("Share Plan", use_container_width=True):
            st.info("📤 Share functionality coming soon!")


def render_results_section(final_state):
    """
    Render complete results section.
    Main function to display all results.
    """
    render_results_header()
    render_action_buttons()
    render_trip_metrics(final_state)
    
    # Tabbed results
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Overview", 
        "🗓️ Day-by-Day Itinerary", 
        "💰 Budget Breakdown", 
        "✈️ Travel Essentials",
        "🎒 Packing List"
    ])
    
    with tab1:
        render_overview_tab(final_state)
    
    with tab2:
        render_itinerary_tab(final_state)
    
    with tab3:
        render_budget_tab(final_state)
    
    with tab4:
        render_essentials_tab(final_state)
    
    with tab5:
        render_packing_tab(final_state)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    
    render_feedback_section()