import preprocessor
import streamlit as st
import helper
import matplotlib.pyplot as plt
import seaborn as sns


st.sidebar.title("Whatsapp Chat Analysis ~ Tech Sarwesh 😉")

uploaded_file = st.sidebar.file_uploader("Choose a File 😀")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.dataframe(df)

    #fetch unique user
    user_list = df['user'].unique().tolist()
    user_list.remove('group notofication')
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user = st.sidebar.selectbox("Show Analysis With Respect To 😁",user_list)

    if st.sidebar.button("Show Analysis 📈"):


        num_message,words,num_media_messages,num_links= helper.fetch_stats(selected_user,df)
        st.title("Top Statisstics of Whatsapp chat 📊")

        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.header("Total Messages📧")
            st.title(num_message)
        with col2:
            st.header("Total Words🔤")
            st.title(words)
        with col3:
            st.header("Media Shared📂")
            st.title(num_media_messages)
        with col4:
            st.header("Link Shared🔗")
            st.title(num_links)

    if selected_user == "Overall":
        st.title("Most Busy User")
        x,new_df= helper.most_busy_users(df)  # Example DataFrame to work with


        fig, ax = plt.subplots()

        # Define colors for each bar
        colors = ['#FF5733', '#33FF57', '#3357FF', '#FF33A8', '#FFC300']

        # Ensure that you only use as many colors as there are bars
        num_bars = len(x)
        if num_bars > len(colors):
            colors += ['#000000'] * (num_bars - len(colors))  # Add more colors if needed

        # Create the bar chart with different colors
        for i, (index, value) in enumerate(zip(x.index, x.values)):
            ax.bar(index, value, color=colors[i], label=f'{index}')  # Assign unique color for each bar

       # Add legend
        ax.legend(title='Users')

       # Optionally, set labels and title
        ax.set_xlabel('Users')
        ax.set_ylabel('Activity Level')
        ax.set_title('Most Busy Users')

        # Streamlit columns
        col1, col2 = st.columns(2)

        with col1:
            st.pyplot(fig)  # Display the figure in Streamlit

        with col2:
            st.dataframe(new_df)
    most_common_df = helper.most_common_words(selected_user,df)

    st.dataframe(most_common_df)


    fig,ax = plt.subplots()
    ax.bar(most_common_df[0],most_common_df[1],color = 'orange')
    plt.xticks(rotation = 'vertical')
    st.title("Most Common Words")
    st.pyplot(fig)

    emoji_df = helper.emoji_helper(selected_user,df)
    st.title("Emoji Analysis")

    col1,col2 = st.columns(2)

    with col1:
        st.dataframe(emoji_df)
    with col2:
        fig,ax = plt.subplots()
        ax.pie(emoji_df[1].head(),labels = emoji_df[0].head(),autopct = "%0.2f")
        st.pyplot(fig)

    st.title("Monthly Timeline Analysis")
    timeline = helper.monthly_timeline(selected_user,df)

    fig,ax = plt.subplots()

    ax.plot(timeline['time'],timeline['message'],color = 'red')
    plt.xticks(rotation = 'vertical')
    st.pyplot(fig)

    #dailytimeline
    st.title("Daily Timeline Analysis")
    daily_timeline = helper.daily_timeline(selected_user,df)
    fig,ax = plt.subplots()

    ax.plot(daily_timeline['only_date'],daily_timeline['message'],color = 'green')
    plt.xticks(rotation = 'vertical')
    st.pyplot(fig)

    st.title("Activity Map")
    col1,col2 = st.columns(2)

    with col1:
        st.header("Most Busy Day")
        busy_day = helper.week_activity_map(selected_user,df)

        fig,ax = plt.subplots()
        ax.bar(busy_day.index,busy_day.values,color = "blue")
        plt.xticks(rotation = "vertical")
        st.pyplot(fig)
    with col2:
        st.header("Most Busy Month")
        busy_month = helper.month_activity_map(selected_user,df)

        fig,ax = plt.subplots()
        ax.bar(busy_month.index,busy_month.values,color = "yellow")
        plt.xticks(rotation = "vertical")
        st.pyplot(fig)
    st.title("Online Activity Map")
    user_heatmap = helper.activity_heatmap(selected_user,df)
    fig,ax = plt.subplots()
    ax = sns.heatmap(user_heatmap)
    st.pyplot(fig)