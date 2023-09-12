from app import db
from app.models import Topic

g_to_g_topics = ['A New Heaven and a New Earth', 'Adoration', 'Aging', 'Animals', 'Assurance', 'Atonement', 'Baptism', 'Care of Creation', 'Celebrating', 'Time', 'Children', 'Christ\'s Return', 'Christ\'s Return and Judgment', 'Christian Life', 'Christian Year', 'Comfort', 'Commitment', 'Communion', 'Community in Christ', 'Compassion', 'Confession', 'Creation', 'Death', 'Dedication', 'Dedication and Stewardship', 'Discipleship', 'Discipleship and Mission', 'Dying in Christ', 'Ecumenical', 'Encouragement', 'Eternal Life', 'Eucharist', 'Evangelism', 'Evening', 'Faith', 'Faithfulness', 'Family', 'Forgiveness', 'Freedom', 'Funeral', 'Gathering', 'Gift of the Holy Spirit', 'God\'s Covenant with Israel', 'Grace', 'Grief', 'Guidance', 'Harvest', 'Healing', 'Hope', 'Humility', 'Hunger', 'Incarnation', 'Invitation', 'Jesus Christ', 'Joy' 'Judgment', 'Justice', 'Justice and Reconciliation', 'Kingdom of God', 'Lament', 'Lament and Longing for Healing', 'Light', 'Living And Dying In Christ', 'Living in Christ Living in God', 'Lord\'s Supper', 'Love for God', 'Love for Others', 'Love of God for Us', 'Mercy', 'Ministry', 'Mission', 'Morning Music and the Arts', 'Obedience', 'Offering', 'Ordination/Installation', 'Personal Peace', 'Praise', 'Prayer', 'Providence', 'Reconciliation' 'Redemption', 'Renewal', 'Repentance', 'Rest', 'Sabbath', 'Salvation', 'Scripture', 'Sending', 'Service', 'Service Music', 'Sin', 'Social Concerns', 'Sovereignty of God', 'Stewardship', 'Teaching/Education', 'Temptation', 'Thanksgiving', 'The Church', 'The Life of the Nations', 'The Triune God', 'The Word', 'Trust', 'Trusting in the Promises of God', 'Truth', 'Unity', 'Vocation', 'Wedding', 'Welcome', 'Will of God', 'Wisdom', 'Women' 'Work', 'World Peace', 'Youth']

for i in range(len(g_to_g_topics)):
    db.session.add(Topic(topic= g_to_g_topics[i]))

db.session.commit()

