from app.dynamo import DynamoDBQuery
import pandas as pd
from app.models.collaborative_filtering import MatrixFactorization
import modelbit
import os


def recommend():
    os.environ["AWS_ACCESS_KEY_ID"] = "AKIA5HPKATSKPD7NFGAS"
    os.environ["AWS_SECRET_ACESS_KEY"] = "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"
    
    combined_data = []
    all_recommendations = {}
    try:
        query = DynamoDBQuery(region_name="ap-southeast-2", table_name="nc-table")
        raw_result = query.execute_query()
        print(raw_result)
        df = pd.DataFrame(raw_result)
        
        combined_data.append(df)
        
        combined_df = pd.concat(combined_data, ignore_index=True)
        combined_df = combined_df.drop_duplicates(subset=['UserID', 'PlaceID'], keep='first')
        combined_df = combined_df[["UserID", "PlaceID", "Rating"]]
        combined_df["Rating"] = combined_df["Rating"].astype(float)
        print(combined_df)

        model = MatrixFactorization(combined_df, K=3, gamma=0.0007, lamda=0.01, steps=100)
        model.train()
        predictions = model.predict()

        for user_id in predictions.index:
            top_n = predictions.loc[user_id].sort_values(ascending=False).head(3)
            all_recommendations[user_id] = top_n.index.tolist()  # Capture only place IDs

        print(all_recommendations)
        return {"recommendations": all_recommendations}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}
    