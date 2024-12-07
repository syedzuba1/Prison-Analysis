import pandas as pd
import pickle
from django.shortcuts import render
from .forms import EconomicImpactForm,CustomUserChangeForm,UserChangeForm,CustomUserCreationForm,AdaptationPredictionForm, CrimePredictionForm, BudgetPredictionForm
import numpy as np
import joblib
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import UserProfile
from django.db import IntegrityError
from django.contrib.auth import logout
from .models import Prediction1,Prediction3,Prediction2,Prediction4
#with open('predictions/models/preprocessing.pkl', 'rb') as file:
#    preprocessor1 = pickle.load(file)
with open('predictions/models/logistic_regression_model.pkl', 'rb') as file:
    model1 = pickle.load(file)

# Load the models and scaler
def load_pickle_files():
    with open('predictions/models/preprocessing_scaler.pkl', 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)
    
    with open('predictions/models/ridge_model_escapees.pkl', 'rb') as escapee_model_file:
        ridge_model_escapees = pickle.load(escapee_model_file)
    
    with open('predictions/models/ridge_model_mental.pkl', 'rb') as mental_model_file:
        ridge_model_mental = pickle.load(mental_model_file)
    
    return scaler, ridge_model_escapees, ridge_model_mental

def load_model_and_scaler():
    with open('trained_model.pkl', 'rb') as model_file:
        model, scaler = pickle.load(model_file)
    return model, scaler

def load_preprocessed_data():
    with open('preprocessed_data.pkl', 'rb') as data_file:
        preprocessed_data = pickle.load(data_file)
    return preprocessed_data



# Load the model, scaler, and dataset once to avoid reloading on every request
with open("predictions/models/crime_model.pkl", "rb") as f:
    model, scaler, combined_df = pickle.load(f)

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        # Pass the POST data and user instance to the form
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            # Save the user instance
            user = form.save(commit=False)
            user.save()
            # Save or update the age in UserProfile
            if hasattr(user, 'userprofile'):
                user.userprofile.age = form.cleaned_data['age']
                user.userprofile.save()
            else:
                UserProfile.objects.create(user=user, age=form.cleaned_data['age'])

            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        # Prepopulate the form, including age from UserProfile
        initial_data = {}
        if hasattr(request.user, 'userprofile'):
            initial_data['age'] = request.user.userprofile.age
        form = CustomUserChangeForm(instance=request.user, initial=initial_data)

    return render(request, 'edit_profile.html', {'form': form})

def Home(request):
    return redirect('dashboard')
    
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

# Define mappings based on training
age_group_mapping = {
    '16-18 years': 0,
    '18-30 years': 1,
    '30-50 years': 2,
    'Above 50 years': 3
}

gender_mapping = {
    'Male': 0,
    'Female': 1
}

def predict_view_1(request):
    result = None
    if request.method == 'POST':
        form = EconomicImpactForm(request.POST)
        if form.is_valid():
            # Extract data from form
            cleaned_data = form.cleaned_data
            age = cleaned_data['age']
            gender = cleaned_data['gender']

            # Determine the age group
            if age < 16:
                result = "Error: Age must be 16 or older."
                return render(request, 'predict_1.html', {'form': form, 'result': result})
            elif 16 <= age <= 18:
                age_group = '16-18 years'
            elif 18 < age <= 30:
                age_group = '18-30 years'
            elif 30 < age <= 50:
                age_group = '30-50 years'
            else:
                age_group = 'Above 50 years'

            # Map inputs to encoded format
            gender_encoded = gender_mapping.get(gender)
            age_group_encoded = age_group_mapping.get(age_group)

            # Create input DataFrame for the model
            transformed_data = pd.DataFrame([[gender_encoded, age_group_encoded]], columns=['Gender', 'Age Group'])

            # Make prediction
            prediction = model1.predict(transformed_data)[0]
            Prediction1.objects.create(
                user=request.user,  # Logged-in user
                age=age,
                gender=gender,
                age_group=age_group,
                prediction='Undertrial' if prediction == 1 else 'Convicted'
            )
            # Format the result
            result = f"Predicted Status: {'Undertrial' if prediction == 1 else 'Convicted'}"
    else:
        form = EconomicImpactForm()

    return render(request, 'predict_1.html', {'form': form, 'result': result})


def predict_view_2(request):
    result = None
    if request.method == 'POST':
        form = AdaptationPredictionForm(request.POST)
        if form.is_valid():
            # Extract data from the form
            cleaned_data = form.cleaned_data
            total_education_facilities = cleaned_data['total_education_facilities']
            escapee_rate = cleaned_data['escapee_rate']
            mental_illness_rate = cleaned_data['mental_illness_rate']

            # Prepare data in the same format as the training data
            input_data = pd.DataFrame([{
                'total_education_facilities': total_education_facilities,
                'escapee_rate': escapee_rate,
                'mental_illness_rate': mental_illness_rate
            }])

            # Load the models and scaler
            scaler, ridge_model_escapees, ridge_model_mental = load_pickle_files()

            # Preprocess the data using the scaler (standardize the features)
            input_data_scaled = scaler.transform(input_data)

            # Predict escapees and mental illness using the models
            predicted_escapees = ridge_model_escapees.predict(input_data_scaled)
            predicted_mental_illness = ridge_model_mental.predict(input_data_scaled)

            # Format the result
            result = {
                'predicted_escapees': f"Predicted number of escapees: {predicted_escapees[0]:.2f}",
                'predicted_mental_illness': f"Predicted number of mental illness cases: {predicted_mental_illness[0]:.2f}"
            }

            Prediction2.objects.create(
                user=request.user,  # Logged-in user
                total_education_facilities=total_education_facilities,
                escapee_rate=escapee_rate,
                mental_illness_rate=mental_illness_rate,
                predicted_escapees=predicted_escapees[0],
                predicted_mental_illness=predicted_mental_illness[0]
            )

    else:
        form = AdaptationPredictionForm()

    return render(request, 'predict_adaptation.html', {'form': form, 'result': result})

def predict_view_3(request):
    result = None
    if request.method == 'POST':
        form = CrimePredictionForm(request.POST)
        if form.is_valid():
            # Extract the form data
            cleaned_data = form.cleaned_data
            state = cleaned_data['state']
            crime_type = cleaned_data['crime_type']

            # Filter data for the given state and crime type
            filtered_df = combined_df[(combined_df['STATE/UT'] == state) & (combined_df['CRIME HEAD'] == crime_type)]
            
            if filtered_df.empty:
                result = f"No data available for state: {state} and crime type: {crime_type}"
            else:
                # Prepare features for prediction
                feature_data = filtered_df[['Grand Total_convicted', 'Grand Total_undertrial']].values
                
                # Preprocess the data using the scaler
                input_data_scaled = scaler.transform(feature_data)

                # Make prediction using the trained model
                prediction = model.predict(input_data_scaled)
                prediction_proba = model.predict_proba(input_data_scaled)

                # Format the result
                status = "Convicted" if prediction[0] == 1 else "Undertrial"
                confidence = max(prediction_proba[0]) * 100
                result = f"Prediction: {status} (Confidence: {confidence:.2f}%)"
                
                Prediction3.objects.create(
                    user=request.user,  # Logged-in user
                    state=state,
                    crime_type=crime_type,
                    predicted_status=status,
                    confidence=confidence
                )
    else:
        form = CrimePredictionForm()
        
    return render(request, 'predict_form.html', {'form': form, 'result': result})

MODEL_PATH = 'predictions/models/budget_prediction_model.pkl'
with open(MODEL_PATH, 'rb') as f:
    model4 = pickle.load(f)


def predict_view_4(request):
    result = None

    if request.method == 'POST':
        form = BudgetPredictionForm(request.POST)
        if form.is_valid():
            # Extract form data
            state_ut = form.cleaned_data['state_ut'].upper()
            year = form.cleaned_data['year']
            num_years = form.cleaned_data['num_years']

            

            input_data = pd.DataFrame({
                'STATE/UT': [state_ut],  # Wrap in a list
                'Year': [year],          # Wrap in a list
                'num_years': [num_years] # Wrap in a list
            })
            
            try:
                # Directly predict using the model
                predicted_budgets = model4.predict(input_data)
                
                result = f"Predicted budgets: {predicted_budgets[0]}"

                Prediction4.objects.create(
                    user=request.user,  # Logged-in user
                    state_ut=state_ut,
                    year=year,
                    num_years=num_years,
                    predicted_budget=predicted_budgets[0]
                )
            except Exception as e:
                result = f"Error during prediction: {str(e)}"
    else:
        form = BudgetPredictionForm()
    return render(request, 'predict_lstm_form.html', {'form': form, 'result': result,})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                # Create the user instance without saving to the database
                user = form.save(commit=False)

                # Populate additional fields from the cleaned_data
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.email = form.cleaned_data['email']
                user.save()  # Save user instance to the database

                # Save the age in the associated UserProfile
                user_profile, created = UserProfile.objects.get_or_create(user=user)
                user_profile.age = form.cleaned_data['age']
                user_profile.save()

                messages.success(request, 'Your account has been created successfully!')
                return redirect('login')  # Redirect to login page after registration
            except IntegrityError:
                messages.error(request, 'An error occurred while creating your profile. Please try again.')
        else:
            messages.error(request, 'There was an error in your form. Please correct the errors and try again.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})
        
def addition(request):
    return render(request, 'addition.html')
@login_required

def logout_and_delete_profile(request):
    # Get the currently logged-in user
    user = request.user

    # Log out the user
    logout(request)

    # Delete the user profile and the user itself
    if hasattr(user, 'userprofile'):
        user.userprofile.delete()  # Delete the related UserProfile if it exists
    user.delete()  # Delete the User

    # Redirect to the login page or any other page
    return redirect('login')  # Replace 'login' with your desired URL name