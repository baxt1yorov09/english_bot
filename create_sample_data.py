import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cefr_bot.settings')
django.setup()

# Sample Speaking Questions
from apps.speaking.models import SpeakingQuestion
from apps.accounts.models import CEFRLevel

def create_sample_speaking_questions():
    questions = [
        # Part 1 Questions
        SpeakingQuestion(
            part='1',
            question_text="Where are you from?",
            level=CEFRLevel.A1,
            time_limit=30
        ),
        SpeakingQuestion(
            part='1',
            question_text="What do you do? Are you a student or do you work?",
            level=CEFRLevel.A1,
            time_limit=30
        ),
        SpeakingQuestion(
            part='1',
            question_text="What do you like doing in your free time?",
            level=CEFRLevel.A1,
            time_limit=30
        ),
        SpeakingQuestion(
            part='1',
            question_text="Why are you learning English?",
            level=CEFRLevel.A2,
            time_limit=30
        ),
        SpeakingQuestion(
            part='1',
            question_text="How long have you been learning English?",
            level=CEFRLevel.A2,
            time_limit=30
        ),
        
        # Part 1.2 Questions (with pictures)
        SpeakingQuestion(
            part='1.2',
            question_text="Compare these two pictures and say what you see.",
            picture1_url="https://picsum.photos/seed/office1/300/200.jpg",
            picture2_url="https://picsum.photos/seed/office2/300/200.jpg",
            level=CEFRLevel.B1,
            time_limit=30
        ),
        SpeakingQuestion(
            part='1.2',
            question_text="Which place would you prefer to work in and why?",
            picture1_url="https://picsum.photos/seed/office1/300/200.jpg",
            picture2_url="https://picsum.photos/seed/office2/300/200.jpg",
            level=CEFRLevel.B1,
            time_limit=30
        ),
        
        # Part 2 Questions (Situations)
        SpeakingQuestion(
            part='2',
            question_text="You want to move abroad for work. Talk about the advantages and problems you might face.",
            level=CEFRLevel.B1,
            time_limit=120
        ),
        SpeakingQuestion(
            part='2',
            question_text="Describe a memorable holiday you had. Where did you go and what did you do?",
            level=CEFRLevel.B1,
            time_limit=120
        ),
        SpeakingQuestion(
            part='2',
            question_text="Talk about a skill you would like to learn. Why is it important and how would you learn it?",
            level=CEFRLevel.B2,
            time_limit=120
        ),
        
        # Part 3 Questions (Topics with Pros/Cons)
        SpeakingQuestion(
            part='3',
            question_text="Discuss online education.",
            pros="Flexible schedule, cheaper, access to global resources, learn at own pace",
            cons="Less interaction, requires self-discipline, technical issues, limited networking",
            level=CEFRLevel.B2,
            time_limit=120
        ),
        SpeakingQuestion(
            part='3',
            question_text="Discuss social media impact on society.",
            pros="Connect people globally, information sharing, business opportunities, awareness",
            cons="Addiction, privacy concerns, fake news, mental health issues",
            level=CEFRLevel.B2,
            time_limit=120
        ),
        SpeakingQuestion(
            part='3',
            question_text="Discuss artificial intelligence in daily life.",
            pros="Efficiency, convenience, automation, problem solving",
            cons="Job displacement, privacy concerns, dependency, ethical issues",
            level=CEFRLevel.C1,
            time_limit=120
        ),
    ]
    
    SpeakingQuestion.objects.bulk_create(questions, ignore_conflicts=True)
    print(f"Created {len(questions)} speaking questions")

# Sample Writing Questions
from apps.writing.models import WritingQuestion

def create_sample_writing_questions():
    questions = [
        # Part 1.1 - Informal Letters
        WritingQuestion(
            task_type='1.1',
            question_text="Your friend is moving to your city. Write a letter to give them advice about living there.",
            level=CEFRLevel.B1,
            min_word_count=50,
            max_word_count=100,
            time_limit_minutes=15,
            sample_answer="Hi [Friend's Name],\n\nI was so excited to hear you're moving here! Let me give you some advice about living in our city. The public transport is great, so you won't need a car. The city center has lots of nice cafes and parks. For housing, I recommend looking in the downtown area - it's convenient and safe.\n\nHope to see you soon!\n\n[Your name]"
        ),
        WritingQuestion(
            task_type='1.1',
            question_text="Write a letter to your friend telling them about a recent holiday you took.",
            level=CEFRLevel.A2,
            min_word_count=50,
            max_word_count=100,
            time_limit_minutes=15
        ),
        
        # Part 1.2 - Formal Letters
        WritingQuestion(
            task_type='1.2',
            question_text="Write to your manager requesting a week off for a family emergency.",
            level=CEFRLevel.B2,
            min_word_count=120,
            max_word_count=150,
            time_limit_minutes=25,
            sample_answer="Dear [Manager's Name],\n\nI am writing to formally request one week of leave from [start date] to [end date] due to a family emergency that requires my immediate attention.\n\nI have ensured that all my current projects are up to date and have briefed [colleague's name] to handle any urgent matters during my absence. I will also be available via email for any critical issues that may arise.\n\nI apologize for any inconvenience this may cause and appreciate your understanding in this matter.\n\nSincerely,\n[Your name]"
        ),
        WritingQuestion(
            task_type='1.2',
            question_text="Write to your university department suggesting improvements to the library facilities.",
            level=CEFRLevel.B2,
            min_word_count=120,
            max_word_count=150,
            time_limit_minutes=25
        ),
        
        # Part 2 - Essays
        WritingQuestion(
            task_type='2',
            question_text="Some people believe that technology has made our lives more complex, while others think it has simplified them. Discuss both views and give your opinion.",
            level=CEFRLevel.B2,
            min_word_count=180,
            max_word_count=250,
            time_limit_minutes=40,
            sample_answer="Technology has become an integral part of modern life, sparking debate about whether it simplifies or complicates our existence. This essay will examine both perspectives before offering my own viewpoint.\n\nOn one hand, technology has undoubtedly simplified many aspects of daily life. Communication across vast distances now takes seconds, online banking eliminates the need for physical visits, and smart home devices automate routine tasks. These conveniences save time and reduce effort, allowing people to focus on more meaningful activities.\n\nHowever, technology also introduces complexity. The constant need to update software, protect against cyber threats, and learn new interfaces can be overwhelming. Moreover, the abundance of digital information creates decision fatigue, and social media pressure adds psychological stress.\n\nIn my opinion, technology is a double-edged sword that requires mindful usage. While it offers incredible benefits, we must establish healthy boundaries to prevent it from overcomplicating our lives. The key lies in leveraging technology as a tool rather than becoming dependent on it."
        ),
        WritingQuestion(
            task_type='2',
            question_text="Environmental problems are too big for individuals to solve. Only governments and large companies can make a difference. To what extent do you agree or disagree?",
            level=CEFRLevel.C1,
            min_word_count=180,
            max_word_count=250,
            time_limit_minutes=40
        ),
        WritingQuestion(
            task_type='2',
            question_text="Some people think that cultural traditions will be destroyed as technology develops. Others believe technology will help preserve traditions. Discuss both views and give your opinion.",
            level=CEFRLevel.B2,
            min_word_count=180,
            max_word_count=250,
            time_limit_minutes=40
        ),
    ]
    
    WritingQuestion.objects.bulk_create(questions, ignore_conflicts=True)
    print(f"Created {len(questions)} writing questions")

if __name__ == "__main__":
    create_sample_speaking_questions()
    create_sample_writing_questions()
