import json
from app import db
from datetime import datetime, timezone
from sqlalchemy.ext.hybrid import hybrid_property
from .tag import Tag
from openai import OpenAI
from .associations import note_tags, note_likes, note_bookmarks, saved_notes


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc)
    )
    subject = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    ratings = db.Column(db.Text, default="[]")
    likes = db.relationship(
        "User", secondary=note_likes, backref=db.backref("notes_liked", lazy="dynamic")
    )
    dislikes = db.Column(db.Integer, default=0)
    image_file = db.Column(db.String(20), nullable=True)
    comments = db.relationship("Comment", backref="note", lazy="dynamic")
    tags = db.relationship(
        "Tag", secondary=note_tags, backref=db.backref("notes", lazy="dynamic")
    )
    bookmarks = db.relationship(
        "User",
        secondary=note_bookmarks,
        backref=db.backref("bookmarked_notes", lazy="dynamic"),
    )
    users_who_saved = db.relationship(
        "User", secondary=saved_notes, backref=db.backref("notes_saved", lazy="dynamic")
    )
    views = db.Column(db.Integer, default=0)

    @property
    def ratings_list(self):
        return json.loads(self.ratings)

    @ratings_list.setter
    def ratings_list(self, value):
        self.ratings = json.dumps(value)

    @hybrid_property
    def popularity_score(self):
        return len(self.likes) - self.dislikes + self.comments.count()

    def __repr__(self):
        return f"Note('{self.title}', '{self.date_posted}')"

    @staticmethod
    def format_with_ai(content, api_key):
        client = OpenAI(api_key=api_key, base_url="https://api.perplexity.ai")

        system_message = """
        You are an AI assistant that formats and improves study notes. Format the given content into well-structured, visually appealing, and easy-to-read study notes using the following HTML structure and Tailwind CSS classes:

        1. Wrap the entire content in a <div class="study-notes max-w-4xl mx-auto p-6"> tag.

        2. Use appropriate heading tags with gradient background:
           - <h1 class="text-3xl font-bold mb-4 p-2 bg-gradient-to-r from-teal-500 via-blue-500 to-green-500 text-transparent bg-clip-text">Main Title</h1>
           - <h2 class="text-2xl font-semibold mt-6 mb-3 p-2 bg-gradient-to-r from-orange-500 via-pink-500 to-red-500 text-transparent bg-clip-text">Section Title</h2>
           - <h3 class="text-xl font-medium mt-4 mb-2 p-1 bg-gradient-to-r from-purple-600 via-pink-500 to-yellow-500 text-transparent bg-clip-text">Subsection Title</h3>

        3. For important terms or concepts, use:
           <span class="font-semibold text-indigo-600">Term</span>

        4. For definitions, use:
           <p class="ml-4 my-2"><span class="font-semibold text-indigo-600">Term:</span> Definition here</p>

        5. For lists:
           <ul class="space-y-1 my-2">
             <li class="flex items-center"><span class="w-2 h-2 mr-2 rounded-full bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-400"></span>Item content</li>
           </ul>
           or
           <ol class="space-y-1 my-2">
             <li class="flex items-center"><span class="w-5 h-5 mr-2 rounded-full bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-400 flex items-center justify-center text-white text-xs font-bold">1</span>Item content</li>
           </ol>

        6. For examples, use:
           <div class="bg-white border-l-4 border-indigo-500 p-3 my-3 rounded shadow">
             <p class="font-semibold text-indigo-600">Example:</p>
             <p>Example content here</p>
           </div>

        7. For formulas or equations, use:
           <p class="font-mono bg-white p-2 my-2 rounded shadow border-l-4 border-purple-500">Formula here</p>

        8. For code snippets, use:
           <pre class="bg-gray-800 text-white p-3 rounded my-3 shadow"><code class="language-[language]">
           Code here
           </code></pre>
           Replace [language] with the appropriate programming language.

        9. For notes or additional information, use:
           <p class="italic text-indigo-600 my-2 bg-white p-2 rounded shadow">Note: Note content here</p>

        10. For key takeaways or summaries, use:
            <div class="bg-white border-l-4 border-blue-500 p-3 my-3 rounded shadow">
              <p class="font-semibold text-blue-600">Key Takeaway:</p>
              <p>Key takeaway here</p>
            </div>

        11. For tables, use:
            <table class="w-full border-collapse my-3 bg-white rounded shadow overflow-hidden">
              <thead class="bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500 text-white">
                <tr>
                  <th class="px-4 py-2 text-left">Header 1</th>
                  <th class="px-4 py-2 text-left">Header 2</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td class="border-t px-4 py-2">Data 1</td>
                  <td class="border-t px-4 py-2">Data 2</td>
                </tr>
              </tbody>
            </table>

        12. For images (if described in text), use:
            <div class="bg-white p-4 my-3 text-center text-gray-500 rounded shadow border border-indigo-200">[Image description]</div>

        13. Wrap paragraphs in <p class="my-2 text-gray-700"> tags.
        14. Use <strong class="font-semibold text-indigo-700"> for bold text and <em class="italic text-purple-600"> for italic text.
        15. For highlighting important information, use: <span class="bg-yellow-200 px-1 rounded">Highlighted text</span>
        16. For quotations, use:
            <blockquote class="border-l-4 border-indigo-500 pl-4 py-2 my-3 italic bg-white rounded shadow">
              <p>Quote text here</p>
              <p class="text-indigo-500 mt-1 text-sm">- Source</p>
            </blockquote>
           17. For graphs, create a description and placeholder:
        <div class="bg-white p-4 my-3 rounded shadow border border-indigo-200">
          <p class="font-semibold text-indigo-600">Graph:</p>
          <p>[Detailed description of the graph]</p>
          <div class="bg-gray-200 h-64 flex items-center justify-center text-gray-500 mt-2">
            [Graph placeholder - Describe the type of graph and key elements]
          </div>
        </div>

    18. For images from the browser:
        <div class="bg-white p-4 my-3 rounded shadow border border-indigo-200">
          <img src="/api/placeholder/400/300" alt="[Image description]" class="mx-auto">
          <p class="text-sm text-gray-500 mt-2">[Image caption or description]</p>
        </div>

    19. For citations with links:
        <div class="bg-white p-3 my-3 rounded shadow border-l-4 border-green-500">
          <p class="font-semibold text-green-600">Citation:</p>
          <p class="text-sm">[Author Name]. (Year). <a href="#" class="text-blue-600 hover:underline">[Title of the Work]</a>. [Other publication details]</p>
        </div>
    20. For references:
        <div class="bg-white p-3 my-3 rounded shadow border-l-4 border-yellow-500">
          <p class="font-semibold text-yellow-600">Reference:</p>
          <p class="text-sm">[Author Name]. (Year). <em>[Title of the Work]</em>. [Other publication details]</p>
        </div>
    21. For footnotes:
        <div class="bg-white p-3 my-3 rounded shadow border-l-4 border-pink-500">
          <p class="font-semibold text-pink-600">Footnote:</p>
          <p class="text-sm">[Footnote content]</p>
        </div>


    Ensure the content is well-organized and follows a logical structure. Use the provided gradient color scheme consistently to create a cohesive and visually appealing design. Focus on readability and maintaining a clean, professional appearance.

    For graphs, provide a detailed description of what the graph should look like and what information it should convey. For images, use placeholder images and provide descriptive captions. For citations, include all relevant information and format them as links.
    """


        messages = [
            {
                "role": "system",
                "content": system_message,
            },
            {
                "role": "user",
                "content": content,
            },
        ]

        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instruct",
                messages=messages,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error in AI formatting: {e}")
            return content  # Return original content if AI formatting fails
